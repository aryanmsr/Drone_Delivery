from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd
import time

class Warehouse():

    def __init__(self, num, x, y, amounts, weight_product_types):
        # amounts - list of every product type amount, some are zero if that product type is not available
        # weight_product_types - weights of product types in this warehouse
        self.num = num
        self.position = (x, y) 
        # self.prod_type =
        # self.prod_amounts = pd.DataFrame({"Amounts": amounts, "Weights": weight_product_types})
        # self.amounts, self.types = self.prod_amounts['Amounts'].values, self.prod_amounts['Amounts'].index.values
        self.amounts = np.array(amounts)
        self.types = np.arange(400)
        self.avail_products = (self.amounts>0)
        # self.all = 1
        self.tot_amounts = self.amounts.sum()
        self.not_avail = False
    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'position: ' + str(self.position) + ', ' + 'tot_amount: ' + str(self.tot_amounts) + ')'

    # Useless?
    def add_product(self, prod_type, prod_qnty):
        self.prod_amounts.append(prod_qnty)

    # TODO: improve this method
    # update number of items of the product type that is removed
    def remove_product(self, prod_type, prod_qnty, warehouses):
        self.amounts[prod_type] -= prod_qnty
        # self.prod_amounts.loc[prod_type, "Amounts"] -= prod_qnty
        # assert np.all(self.amounts == self.prod_amounts["Amounts"].values)
        # self.amounts = self.prod_amounts['Amounts'].values
        self.avail_products = (self.amounts>0)#.sum()
        warehouses.tot_amounts[self.num] = self.amounts.sum()
        warehouses.avail_products[self.num] =  self.avail_products
        assert np.all(self.amounts>=0)
    
    def update_not_avail(self, warehouses): # what does this do?
        self.not_avail = True
        warehouses.not_avail[self.num] = True

        
        
        
    #
    # def find_nearest_order(self, orders):  # dictionary of orders (class Orders)
    #     # o = np.array([orders[x].position for x in orders], dtype=np.float64)
    #     o = orders.positions.astype(np.float64)
    #     # a = np.array([(orders[x].assigned<=2) for x in orders])
    #     c = orders.completed
    #     # c = np.array([orders.dict[x].completed for x in orders.dict])

    #     # check_avail = self.avail_orders
    #     check_avail = np.array([np.all(x.check_avail_types(self.prod_amounts)) for x in orders.dict.values()])
       
    #     # check_avail = np.array([np.all(self.check_avail_types(orders.dict[x].prod_types)) for x in orders.dict])
    #     if c.sum() == 1250:
    #         return 'All orders are completed'
    #     # set distances to infinity of completed orders and orders not available
    #     o[(c)|(~check_avail)] = np.inf
    #     # o[~check_avail] = np.inf
    #     # o[a] = np.inf
    #     d = dist(self.position, o)
    #     nearest_order = orders.dict[np.argmin(d)]
    #     # w = dist(self.position, o.warehouses)
    #     return nearest_order

    # def check_avail_types(self, prod_types):  # prod_types  , prod_qnty
    #     # checking for the type
    #     return self.prod_amounts.loc[prod_types, 'Amounts']>0

    # def select_avail_types(self, prod_types):
    #     return prod_types[self.check_avail_types(prod_types)]

        # return pd.Series(prod_types).isin(self.prod_amounts[self.prod_amounts["Amounts"] > 0].index)
    # def check_quantity(self, prod_types, prod_qnty):
    #     return self.prod_amounts.loc[prod_types, 'Amounts']>prod_qnty

    # def select_avail_quantities(self, prod_types, prod_qnty):
    #     wrhs_qnty = self.prod_amounts.loc[prod_types]
    #     return np.column_stack((wrhs_qnty, prod_qnty)).min(1)
        
    # check product availability only based on quantity
    # def check_avail2(self, prod_type, prod_qnty):
        # checking for the quantity
        # return self.prod_amounts.loc[self.prod_amounts.index == prod_type, "Amounts"].values[0] >= prod_qnty



    #only update the true ones
    def update_availability(self,  warehouses, orders):
        not_completed_orders = np.flatnonzero(~orders.completed)

        # for x in warehouses.dict.values():
        #     if x.amounts.sum()>0:
        #         warehouses.all_avail_orders[x.num][completed_orders] = False
        #         warehouses.any_avail_orders[x.num][completed_orders] = False
        #         if all == 1:
        #             avail_orders_all = np.flatnonzero(warehouses.all_avail_orders[x.num])
        #             warehouses.all_avail_orders[x.num][avail_orders_all] = np.array([np.all(
        #             orders.dict[o].check_avail_types(x)) for o in avail_orders_all])
        #             if not np.any(warehouses.all_avail_orders[x.num]):
        #                 x.all = 0
        #                 warehouses.all[x.num] = 0
        #             else:
        #                 x.all = 1
        #                 warehouses.all[x.num] = 1
        #         else:
        #             avail_orders_any = np.flatnonzero(warehouses.any_avail_orders[x.num])
        #             warehouses.any_avail_orders[x.num][avail_orders_any] = np.array([np.any(
        #             orders.dict[o].check_avail_types(x)) for o in avail_orders_any]) 
        warehouses.all_avail_orders[self.num][orders.completed] = False
        warehouses.any_avail_orders[self.num][orders.completed] = False
        avail_orders_any = np.flatnonzero(warehouses.any_avail_orders[self.num])

        warehouses.all_avail_orders[self.num][not_completed_orders] = np.array([np.all(orders.dict[o].check_avail_types(self)) 
        for o in not_completed_orders]) 
        warehouses.any_avail_orders[self.num][avail_orders_any] = np.array([np.any(orders.dict[o].check_avail_types(self)) 
        for o in avail_orders_any]) 

        # if all == 1:
        #     avail_orders_all = np.flatnonzero(warehouses.all_avail_orders[self.num])
        #     warehouses.all_avail_orders[self.num][avail_orders_all] = np.array([np.all(
        #         orders.dict[o].check_avail_types(self)) for o in avail_orders_all]) 
            
        #     # b = avail_orders_all.shape
        #     # b = [warehouses.all_avail_orders[x].sum() for x in range(9)]

        # else:
        #     avail_orders_any = np.flatnonzero(warehouses.any_avail_orders[self.num])
        #     warehouses.any_avail_orders[self.num][avail_orders_any] = np.array([np.any(
        #         orders.dict[o].check_avail_types(self)) for o in avail_orders_any]) 
        
            # b = avail_orders_any.shape
            # b = [warehouses.any_avail_orders[x].sum() for x in range(9)]
        # return  b
                
class Warehouses():
    def __init__(self, n_wrhs, orders, wrhsdict):
        self.n_wrhs = n_wrhs
        self.dict = wrhsdict
        positions = [wrhsdict[x].position for x in wrhsdict]
        self.tot_amounts = [wrhsdict[x].amounts.sum() for x in wrhsdict]
        self.positions = positions
        self.avail_products = [wrhsdict[x].avail_products for x in wrhsdict]
        self.not_avail = np.array([(wrhsdict[x].not_avail) for x in wrhsdict])
        # self.all = [wrhsdict[x].all for x in wrhsdict]

        self.all_avail_orders = {}
        for w in self.dict.values():
            self.all_avail_orders[w.num] = np.array([np.all(
                o.check_avail_types(w)) for o in orders.dict.values()])

        self.any_avail_orders = {}
        for w in self.dict.values():
            self.any_avail_orders[w.num] = np.array([np.any(
                o.check_avail_types(w)) for o in orders.dict.values()])

    def check_empty(self):
        empty_warehouses = [self.dict[x].amounts.sum() <= 0 for x in self.dict]
        return np.array(empty_warehouses)
