from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd

class Order(object):

    def __init__(self, num, x, y, amount, types, weight_prod_types):
        # x - location
        # y - location
        # amount - total number of items
        # types - [1, 1, 2, 3 4, 4]
        # weight product types - initialized @ beginning of sim

        self.amount = amount
        self.num = num
        self.position = (x, y)
        self.completed = False
        self.turn_order_completed = 0
        self.all_weights = weight_prod_types

        self.typelist = np.array(types)
        # self.prod_amounts = pd.DataFrame(np.unique(self.prod_types, return_counts=True)).T.rename(
        #     columns={0: "Types", 1: "Amounts"})
        self.amounts = np.zeros(400, dtype=np.int32) 
        self.types = np.arange(400, dtype=np.int32)
        t, a = np.unique(self.typelist, return_counts=True)
        self.amounts[t] += a
        self.weights = np.array(weight_prod_types)
        self.prod_amounts = self.amounts[self.amounts>0]
        self.prod_types = self.types[self.amounts>0]
        # self.prod_types, self.prod_amounts = np.unique(self.typelist, return_counts=True)

        # self.weights = np.array(weight_prod_types)[self.prod_types]
        self.tot_weight = np.sum(self.weights*self.amounts)

        # self.df = pd.DataFrame({'Amounts': self.prod_amounts, 'Weights': self.weights*self.prod_amounts},
        #  index = self.prod_types).sort_values('Weights') #sort by weight(?)

        # self.df_repeated = pd.DataFrame({'Amounts': np.ones(self.types.shape), 'Weights': 
        # np.array(self.all_weights)[self.types]}, index = self.types).sort_values('Weights') 

        self.assigned = 0

        # -- Other methods we could have used
        # = collections.Counter(self.prod_types
        # pd.Series(self.prod_types).value_counts()            #number of items per product type
        # self.products_quantity = pd.Series(self.products_type, columns = 'type').groupby('type').count()
        # self.prod_weights = weights[types]

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'n_items: ' + str(
            self.amount) + ', ' + 'tot_weight: ' + str(
                self.tot_weight) + ', ' + 'types: ' + str(self.prod_types) + ', ' + 'quantities: ' + str(
                    self.prod_amounts) + ', ' + 'weights:' + str(self.weights[self.amounts>0]) + ')'


    # TODO: improve remove method, but watch out because it's used in main_sim
    def remove_prod(self, prod_type, prod_qnty):
        self.amounts[prod_type] -= prod_qnty
        # self.df.loc[prod_type, 'Amounts'] -= prod_qnty
        # assert np.all(self.amounts[prod_type] == self.df.loc[prod_type, 'Amounts'])
        # self.df = self.df.loc[self.df['Amounts']>0]
        self.prod_amounts = self.amounts[self.amounts>0]
        # self.prod_types = self.types[self.types[self.amounts>0]]
        self.prod_types = self.types[self.amounts>0]
        # self.df_repeated.loc[prod_type, 'Amounts'] -= prod_qnty
        # self.df_repeated = self.df_repeated[self.df_repeated['Amounts']>0]

        # t = list(self.typelist)
        # for x in list(np.repeat(prod_type, prod_qnty)):
        #     t.remove(x)
        # self.typelist = np.array(t)
        # if self.types.shape[0] == 0:
        #     self.df_repeated = pd.DataFrame({})
        # else: 
        #     self.df_repeated = pd.DataFrame({'Amounts': np.ones(self.types.shape), 'Weights': 
        #     np.array(self.all_weights)[self.types]}, index = self.types).sort_values('Weights') 

        # self.prod_amounts = self.df['Amounts'].values
        # self.prod_types = self.df.index.values
        # self.weights = self.df['Weights'].values//self.prod_amounts

        self.amount -= prod_qnty.sum()
        self.tot_weight = np.sum(self.weights[self.prod_types]*self.amounts[self.prod_types])
        # assert np.all(a==b)
        # self.df_repeated = pd.DataFrame({'Amounts': np.ones(self.types.shape), 'Weights': 
        # np.array(self.all_weights)[self.types]}, index = self.types).sort_values('Weights') 

    # def create_df_repeated(self, types, qnty):
    #     types_repeated = np.repeat(types, qnty)
    #     weights = np.array(self.all_weights)[types_repeated]
    #     amounts = np.ones(types_repeated.shape[0])
    #     df_repeated = pd.DataFrame({'Amounts': amounts, 'Weights': weights}, index = types_repeated).sort_values('Weights')
    #     return df_repeated
        
        

    def check_completed(self, turn, orders):
        if self.amounts.sum() == 0:
            self.completed = True
            self.turn_order_completed = turn
            orders.add_completed(self.num)
            orders.turn_order_completed[self.num] = self.turn_order_completed
        # return self.prod_amounts["Amounts"].sum == 0

    def check_avail_types(self, wrhs):  # prod_types  , prod_qnty
        # checking for the type        
        avail = wrhs.avail_products[self.prod_types]
        return avail
        # return wrhs.amounts[self.prod_types]>0
        # return wrhs.prod_amounts.loc[self.prod_types, 'Amounts']>0


    


class Orders():

    def __init__(self, n_orders, ordersdict):
        positions = [ordersdict[x].position for x in ordersdict]
        self.positions = np.array(positions)
        self.n_orders = n_orders
        self.dict = ordersdict
        completed = [ordersdict[x].completed for x in ordersdict]
        self.completed = np.array(completed)
        self.turn_order_completed = [ordersdict[x].turn_order_completed for x in ordersdict]
        # self.linked_orders = [ordersdict[x].df
        #  for x in ordersdict]

    def __repr__(self):
        return f'n_orders: {self.n_orders}, completed: {self.completed.sum()}'

    def add_completed(self, ordernum):
        self.completed[ordernum] = True

        
        

# ord = Order(1, 23, 34, 5, [1, 1, 2, 3, 4], [1, 1, 1, 1, 1])
