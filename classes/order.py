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
        self.position = [x, y]
        self.completed = False
        self.turn_order_completed = 0

        self.types = np.array(types)
        # self.prod_amounts = pd.DataFrame(np.unique(self.prod_types, return_counts=True)).T.rename(
        #     columns={0: "Types", 1: "Amounts"})
        self.prod_types, self.prod_amounts = np.unique(self.types, return_counts=True)

        self.weights = np.array(weight_prod_types)[self.prod_types]
        self.tot_weight = np.sum(self.weights*self.prod_amounts)

        self.df = pd.DataFrame({'Amounts': self.prod_amounts, 'Weights': self.weights*self.prod_amounts},
         index = self.prod_types).sort_values('Weights') #sort by weight(?)

        self.assigned = 0

        # -- Other methods we could have used
        # = collections.Counter(self.prod_types
        # pd.Series(self.prod_types).value_counts()            #number of items per product type
        # self.products_quantity = pd.Series(self.products_type, columns = 'type').groupby('type').count()
        # self.prod_weights = weights[types]

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'n_items: ' + str(
            self.amount) + ', ' + 'tot_weight: ' + str(self.tot_weight) + ')'

    # TODO: improve remove method, but watch out because it's used in main_sim
    def remove_prod(self, prod_type, prod_qnty):
        self.df.loc[prod_type, 'Amounts'] -= prod_qnty
        self.df = self.df[self.df['Amounts']>0]
        self.prod_amounts = self.df['Amounts']
        self.prod_types = self.df.index.values
        

    def check_completed(self, turn, orders):
        # return self.prod_amounts["Amounts"].sum == 0
        if self.prod_amounts.sum() == 0:
            self.completed = True
            self.turn_order_completed = turn
            orders.add_completed(self.num)
            # print('An order has been completed!')

    def check_avail_types(self, wrhs_df):  # prod_types  , prod_qnty
        # checking for the type
        return wrhs_df.loc[self.prod_types, 'Amounts']>0

    


class Orders():

    def __init__(self, n_orders, ordersdict):
        positions = [ordersdict[x].position for x in ordersdict]
        self.positions = np.array(positions)
        self.n_orders = n_orders
        self.dict = ordersdict
        completed = [ordersdict[x].completed for x in ordersdict]
        self.completed = np.array(completed)

    def __repr__(self):
        return f'n_orders: {self.n_orders}, completed: {self.completed.sum()}'

    def add_completed(self, ordernum):
        self.completed[ordernum] = True
        # print(f'order{ordernum} has been completed!')
        

# ord = Order(1, 23, 34, 5, [1, 1, 2, 3, 4], [1, 1, 1, 1, 1])
# print(ord.prod_amounts)
# print(ord.prod_amounts.loc[ord.prod_amounts["Types"]==1]["Amounts"])
