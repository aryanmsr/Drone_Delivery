from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd
import time
class Warehouse(object):

    def __init__(self, num, x, y, amounts, weight_product_types):
        # amounts - list of every product type amount, some are zero if that product type is not available
        # weight_product_types - weights of product types in this warehouse
        self.num = num
        self.position = [x, y] 
        # self.prod_type =
        self.prod_amounts = pd.DataFrame({"Amounts": amounts, "Weights": weight_product_types})

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'position: ' + str(self.position) + ')'

    # Useless?
    def add_product(self, prod_type, prod_qnty):
        self.prod_amounts.append(prod_qnty)

    # TODO: improve this method
    # update number of items of the product type that is removed
    def remove_product(self, prod_type, prod_qnty):
        self.prod_amounts.loc[prod_type, "Amounts"] -= prod_qnty
        
    #
    # def find_nearest_order(self, orders):  # dictionary of orders (class Orders)
    #     # o = np.array([orders[x].position for x in orders], dtype=np.float64)
    #     o = orders.positions.astype(np.float64)
    #     # a = np.array([(orders[x].assigned<=2) for x in orders])
    #     c = orders.completed
    #     t2 = time.time()
    #     # c = np.array([orders.dict[x].completed for x in orders.dict])

    #     # check_avail = self.avail_orders
    #     check_avail = np.array([np.all(x.check_avail_types(self.prod_amounts)) for x in orders.dict.values()])
       
    #     # check_avail = np.array([np.all(self.check_avail_types(orders.dict[x].prod_types)) for x in orders.dict])
    #     t3 = time.time()
    #     # print(f'check_avail: {t3-t2}')
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

    # TODO consider integrating this check in find_nearest_order

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

# wrh = Warehouse(1, 23, 34, [5, 6, 82, 3, 0], [10, 11, 22, 33, 44])
# wrh.remove_product(2, 10)
# print(wrh.prod_amounts)
# print(wrh.check_avail2(0, 4))
# print(wrh.check_avail2(0, 5))
# print(wrh.check_avail2(0, 6))
class Warehouses():
    def __init__(self, n_wrhs, orders, wrhsdict):
        self.n_wrhs = n_wrhs
        self.dict = wrhsdict
        self.all_avail_orders = {}
        for w in self.dict.values():
            self.all_avail_orders[w.num] = np.array([np.all(
                o.check_avail_types(w.prod_amounts)) for o in orders.dict.values()]) 
        # self.any_avail_orders = {}
        # t = time.time()
        # for w in self.dict.values():
        #     self.any_avail_orders[w.num] = np.array([np.any(
        #         o.check_avail_types(w.prod_amounts)) for o in orders.dict.values()])
        # t1 = time.time()
        # print(t1-t)
