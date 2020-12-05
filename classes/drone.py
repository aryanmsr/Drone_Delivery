from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd

class Drone(object):  # inherit #product #warehouse #order (#utility)

    def __init__(self, num, weight_prod_types):
        self.num = num
        self.prod_types = np.array([],  dtype = np.int32)
        self.prod_amounts = np.array([],  dtype = np.int32)
        self.pld_weight = 0
        self.cur_pos = [0, 0]
        self.turns = 0  # ?
        self.actions = []  # ?
        self.state = 'W'
        self.weights = np.array(weight_prod_types)
        self.df = pd.DataFrame({'Amounts': self.prod_amounts},index = self.prod_types)

        # Df for use throughout
        # self.Data = Dataframes()
        # self.Util = Utility()

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'payload_weight: ' + str(sum(self.prod_types)) + ')'

    def load(self, prod_types, prod_qnty, wrhs):
        self.state = 'L'
        new_df = pd.DataFrame({'Amounts':prod_qnty}, index = prod_types)
        # print(new_df)
        # print(self.df)
        already_existing_types = self.df[self.df.index.isin(new_df.index)].index.values
        # print(new_df.loc[already_existing_types])
        self.df.loc[already_existing_types, 'Amounts'] += new_df.loc[already_existing_types, 'Amounts']
        self.df = pd.concat([self.df, new_df[~new_df.index.isin(self.df.index)]])

        self.prod_types = self.df.index.values
        self.prod_amounts = self.df['Amounts'].values

        # wrhs.remove_product(prod_types, prod_qnty)
        
        # pactions.append([0 L 1 2 3 ]) ?order_number
        for i in range(prod_types.shape[0]):
            print(f'{self.num} {self.state} {wrhs.num} {prod_qnty[i]} {prod_types[i]}')
        self.turns += prod_types.shape[0] 

        # TODO update payload mass

    def unload(self, prod_types, qnty):  # warehouse
        self.prod_types.remove(prod_types)
        self.prod_amounts.remove(qnty)
        # actions.append([0 U 1 2 3 ])?order_number
        self.turns += 1

    def compute_weight(self):
        return self.weights[self.prod_types]*self.prod_amounts
        # tot_weight = 0
        # for i in range(len(self.prod_types)):
        #     unit_weight = self.weights[self.prod_types[i]]
        #     tot_weight += unit_weight * self.prod_amounts[i]
        # self.pld_weight = tot_weight

    def deliver(self, prod_types, prod_qnty, order, orders):  # to the order
        self.state = 'D'
        # pactions.append([0 D 1 2 3 ]) ?order_number
        # print(prod_types.shape[0])
        for i in range(prod_types.shape[0]):
            print(f'{self.num} {self.state} {order.num} {prod_qnty[i]} {prod_types[i]}')
        self.turns += prod_types.shape[0]
        self.df.loc[prod_types, 'Amounts'] -= prod_qnty
        self.df = self.df[self.df['Amounts']>0]

        self.prod_types = self.df.index.values
        self.prod_amounts = self.df['Amounts'].values
        
        # order.remove_prod(prod_types, prod_qnty)
        # order.assigned -=1
        # self.compute_weight()
        # order.check_completed(self.turns, orders)


        # self.prod_types.remove(prod_type)
        # self.prod_amounts.remove(qnty)
        # # actions.append([0 D 1 2 3 ])?order_number
        # self.turns += 1

    def wait(self, n_turns):
        self.state = 'W'
        self.turns += n_turns
        # print(f'{self.num} {self.state} {n_turns}')

    def get_cur_pos(self):
        return self.cur_pos

    def update_cur_pos(self, new_pos):
        self.cur_pos = new_pos  # define in utility class

    # account for distance in the count of turns for delivery

    def find_nearest_wh(self, warehouses):
        wh = np.array([warehouses[x].position for x in warehouses], dtype=np.float64)
        d = dist(self.cur_pos, wh)
        return warehouses[np.argmin(d)]

    def check_pld_weight(self):
        return self.pld_weight <= 200

    #filter the product types which ae available at the warehouse
    def select_avail_types(self, wrhs, order):
        return order.prod_types[order.check_avail_types(wrhs.prod_amounts)]

    #selects the minimum quantity between the that available in the warehouse and the one required in order
    def select_avail_quantities(self, avail_types, order, wrhs):
        wrhs_qnty = wrhs.prod_amounts.loc[avail_types]
        order_qnty = order.df.loc[avail_types, 'Amounts']
        return np.column_stack((wrhs_qnty, order_qnty)).min(1)

    def find_nearest_order(self, orders, warehouses, wrhs):  # dictionary of orders (class Orders)
        order_pos = orders.positions.astype(np.float64)
        c = orders.completed
        check_avail = warehouses.all_avail_orders[wrhs.num]
        # check_avail = warehouses.any_avail_orders[wrhs.num]
        if c.sum() == 1250:
            return 'All orders are completed'
        order_pos[(c)|(~check_avail)] = np.inf
        d = dist(self.cur_pos, order_pos)
        nearest_order = orders.dict[np.argmin(d)]
        return nearest_order

    def assign_order(self, order, wrhs, warehouses):
        # order.assigned += 1        
        avail_types = self.select_avail_types(wrhs, order)
        # avail_types = wrhs.select_avail_types(order.prod_types)
        avail_qnty = self.select_avail_quantities(avail_types, order, wrhs)
        # avail_qnty = wrhs.select_avail_quantities(avail_types, order.df.loc[avail_types, 'Amounts'])
        # print(self.weights[avail_types])
        if np.sum(self.weights[avail_types]*avail_qnty)<=200:
            new_types = avail_types
            new_qnty = avail_qnty
            wrhs.remove_product(avail_types, avail_qnty)
            self.load(avail_types, avail_qnty, wrhs)
            # print('<=200')
        else:
            new_types = order.df.index[order.df['Weights'].cumsum()<200].values
            new_qnty = order.df.loc[new_types, 'Amounts'].values
            # print(self.weights[new_types])
            # print(np.sum(self.weights[new_types]*new_qnty))
            wrhs.remove_product(new_types, new_qnty)
            # print(new_types, self.weights[new_types])
            self.load(new_types, new_qnty, wrhs)
            # print('>200')
        # print(f'qnty: {new_qnty}, type: {new_types}, order.num: {order.num}, order_df: {order.df}')

        # print(f'{warehouses.all_avail_orders[wrhs.num].sum()}')
        # print(f'{warehouses.all_avail_orders[}')

        if not np.all(order.check_avail_types(wrhs.prod_amounts)):
            warehouses.all_avail_orders[wrhs.num][order.num] = False

            # print(f'avail_types of {order.num} has been updated')
        # print(order.check_avail_types(wrhs.prod_amounts))
        # if not np.any(order.check_avail_types(wrhs.prod_amounts)):
        #     warehouses.any_avail_orders[wrhs.num][order.num] = False
        #     print(f'avail_types of {order.num} has been updated')
        return new_types, new_qnty

    def deliver_order(self, types, qnty, order, orders):
        self.turns += np.ceil(dist(self.cur_pos, order.position))
        self.update_cur_pos(order.position)
        # print(self.prod_amounts, self.prod_types)
        self.deliver(types, qnty, order, orders)
        order.remove_prod(types, qnty)
        # order.assigned -= 1
        self.compute_weight()
        order.check_completed(self.turns, orders)

        


    

