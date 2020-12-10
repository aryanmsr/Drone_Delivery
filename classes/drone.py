from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd

class Drone(object):  # inherit #product #warehouse #order (#utility)

    def __init__(self, num, weight_prod_types):
        self.num = num
        # self.prod_types = np.array([],  dtype = np.int32)
        # self.prod_amounts = np.array([],  dtype = np.int32)
        self.pld_weight = 0
        self.cur_pos = [0, 0]
        self.turns = 0  # ?
        self.actions = []  # ?
        self.state = 'W'
        self.weights = np.array(weight_prod_types)
        # self.df = pd.DataFrame({'Amounts': self.prod_amounts},index = self.prod_types)
        self.orders = []
        self.amounts = np.zeros(400)
        self.types = np.arange(400)
        # Df for use throughout
        # self.Data = Dataframes()
        # self.Util = Utility()

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'types: ' + str(self.types[self.amounts>0]) + ', ' + 'amounts: ' +  str(self.amounts[self.amounts>0]) + ')'

    def load(self, prod_types, prod_qnty, wrhs):
        self.state = 'L'
        # new_df = pd.DataFrame({'Amounts':prod_qnty}, index = prod_types)
        # already_existing_types = self.df[self.df.index.isin(new_df.index)].index.values
        # self.df.loc[already_existing_types, 'Amounts'] += new_df.loc[already_existing_types, 'Amounts']
        # self.df = pd.concat([self.df, new_df[~new_df.index.isin(self.df.index)]])

        # self.prod_types = self.df.index.values
        # self.prod_amounts = self.df['Amounts'].values

        self.amounts[prod_types] += 1
        self.compute_weight()
        # wrhs.remove_product(prod_types, prod_qnty)
        
        # pactions.append([0 L 1 2 3 ]) ?order_number
        message = []
        for i in range(prod_types.shape[0]):
            # print(f'{self.num} {self.state} {wrhs.num} {prod_qnty[i]} {prod_types[i]}')
            message.append(f'{self.num} {self.state} {wrhs.num} {prod_qnty[i]} {prod_types[i]}')
        self.turns += prod_types.shape[0] 
        return message
        # TODO update payload mass

    def unload(self, prod_types, qnty):  # TODO
        # self.prod_types.remove(prod_types)
        # self.prod_amounts.remove(qnty)
        # actions.append([0 U 1 2 3 ])?order_number
        self.turns += 1

    def compute_weight(self):
        return self.weights[self.types]*self.amounts[self.types]
        # return self.weights[self.prod_types]*self.prod_amounts
        # tot_weight = 0
        # for i in range(len(self.prod_types)):
        #     unit_weight = self.weights[self.prod_types[i]]
        #     tot_weight += unit_weight * self.prod_amounts[i]
        # self.pld_weight = tot_weight

    def deliver(self, prod_types, prod_qnty, order, orders):  # to the order
        self.state = 'D'
        # pactions.append([0 D 1 2 3 ]) ?order_number
        # print(prod_types.shape[0])
        message = []
        for i in range(prod_types.shape[0]):
            # print(f'{self.num} {self.state} {order.num} {prod_qnty[i]} {prod_types[i]}')
            message.append(f'{self.num} {self.state} {order.num} {prod_qnty[i]} {prod_types[i]}')

        self.turns += prod_types.shape[0]

        self.amounts[prod_types] -= prod_qnty
        self.compute_weight()
        return message 
        # self.df.loc[prod_types, 'Amounts'] -= prod_qnty
        # self.df = self.df[self.df['Amounts']>0]

        # self.prod_types = self.df.index.values
        # self.prod_amounts = self.df['Amounts'].values
        
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
        wh = np.array(warehouses.positions, dtype=np.float64)
        # wh[warehouses.check_empty()|(warehouses.all == 0)] = np.inf
        # if np.min(wh) == np.inf:
            # wh = np.array(warehouses.positions, dtype=np.float64)
        wh[(warehouses.check_empty())|warehouses.not_avail] = np.inf
        d = dist(self.cur_pos, wh)
        return warehouses.dict[np.argmin(d)]

    def check_pld_weight(self):
        return self.pld_weight <= 200

    #filter the product types which ae available at the warehouse
    def select_avail_types(self, wrhs, order):
        avail_types = order.prod_types[order.check_avail_types(wrhs)]
        # avail_types = order.types[]
        return avail_types

    #selects the minimum quantity between the that available in the warehouse and the one required in order
    def select_avail_quantities(self, avail_types, order, wrhs):
        # wrhs_qnty = wrhs.prod_amounts.loc[avail_types, 'Amounts'].values
        wrhs_qnty = wrhs.amounts[avail_types]

        # order_qnty = order.df.loc[avail_types, 'Amounts'].values
        order_qnty = order.amounts[avail_types]
        # assert np.all(order_qnty == order_qnty_) 
        selected_qnty = np.column_stack((wrhs_qnty, order_qnty)).min(1)
        assert np.all(selected_qnty == np.min((wrhs_qnty, order_qnty), 0))
        # print(f'wrhs q: {wrhs_qnty}, order q: {order_qnty}, selected: {selected_qnty}, avail_types: {avail_types}')
        return selected_qnty

    def find_nearest_order(self, orders, warehouses, wrhs):  # dictionary of orders (class Orders)
        if self.orders != []:
            last_order = self.orders[-1]
            if last_order.amount>0 and np.any(last_order.check_avail_types(wrhs)):
                return self.orders[-1], 'last' #54229
        order_pos = orders.positions.astype(np.float64)
        c = orders.completed
        check_avail = warehouses.all_avail_orders[wrhs.num]
        # if check_avail.sum() == 0:
        # check_avail = warehouses.any_avail_orders[wrhs.num]
        if c.sum() == 1250:
            return 'All orders are completed', 'completed'
        order_pos[(c)|(~check_avail)] = np.inf
        # print(f'avail_orders: {np.sum(order_pos==np.inf)}')
        d = dist(self.cur_pos, order_pos)
        if np.min(d) == np.inf:
            order_pos = orders.positions.astype(np.float64)
            check_avail = warehouses.any_avail_orders[wrhs.num]
            order_pos[(c)|(~check_avail)] = np.inf
            d = dist(self.cur_pos, order_pos)
            if np.min(d) == np.inf:
                assert order_pos.min() == np.inf
                wrhs.update_not_avail(warehouses)
            nearest_order = orders.dict[np.argmin(d)]
            return nearest_order, 0
        nearest_order = orders.dict[np.argmin(d)]
        # print((order_pos<np.inf).sum())
        return nearest_order, 1 #53990

    def assign_order(self, order, wrhs, warehouses):
        self.orders.append(order)
        # order.assigned += 1        
        avail_types = self.select_avail_types(wrhs, order)
        # avail_types = wrhs.select_avail_types(order.prod_types)
        avail_qnty = self.select_avail_quantities(avail_types, order, wrhs)
        # avail_qnty = wrhs.select_avail_quantities(avail_types, order.df.loc[avail_types, 'Amounts'])
        if np.sum(self.weights[avail_types]*avail_qnty)<=200:
            new_types = avail_types
            new_qnty = avail_qnty
            # wrhs.remove_product(new_types, new_qnty, warehouses)
            # self.load(new_types, new_qnty, wrhs)
        else:
            # types = np.repeat(avail_types, avail_qnty)
            # weights = 
            types = np.repeat(avail_types, avail_qnty)
            weights = self.weights[types]
            repeated_matrix = np.column_stack((types, weights))
            rep_mat_sorted = repeated_matrix[repeated_matrix[:,1].argsort()]
            
            mask_le200 = rep_mat_sorted[:,1].cumsum() <= 200
            new_types_repeated = rep_mat_sorted[mask_le200][:,0]

            # new_types_repeated = repeated_matrix[repeated_matrix[repeated_matrix[:,1].argsort()][:,1].cumsum()<=200][:,0]
            new_types, new_qnty = np.unique(new_types_repeated, return_counts=True)

            # avail_types_df = order.df.loc[avail_types]
            # new_types = avail_types_df.index[avail_types_df['Weights'].cumsum()<=200].values
            # new_qnty = avail_types_df.loc[new_types, 'Amounts'].values

            # if new_types.shape[0] == 0:
            #     types = np.repeat(avail_types, avail_qnty)
            #     weights = self.weights[types]
            #     repeated_matrix = np.column_stack((types, weights))
            #     new_types_repeated = repeated_matrix[repeated_matrix[repeated_matrix[:,1].argsort()][:,1].cumsum()<=200][:,0]
            #     new_types, new_qnty = np.unique(new_types_repeated, return_counts=True)

                # avail_types_df_repeated = order.create_df_repeated(avail_types, avail_qnty)
                # types_repeated = avail_types_df_repeated.index[avail_types_df_repeated['Weights'].cumsum()<=200].values
        
        wrhs.remove_product(new_types, new_qnty, warehouses)
        loading_message = self.load(new_types, new_qnty, wrhs)
        return new_types, new_qnty, loading_message

        # if not np.all(order.check_avail_types(wrhs.prod_amounts)):
        #     warehouses.all_avail_orders[wrhs.num][order.num] = False


        # if not np.any(order.check_avail_types(wrhs.prod_amounts)):
        #     warehouses.any_avail_orders[wrhs.num][order.num] = False
        # return new_types, new_qnty

    def deliver_order(self, types, qnty, order, orders):
        self.turns += np.int(np.ceil(dist(self.cur_pos, order.position)))
        self.update_cur_pos(order.position)
        delivery_message = self.deliver(types, qnty, order, orders)
        order.remove_prod(types, qnty)
        # order.assigned -= 1
        self.compute_weight()
        order.check_completed(self.turns, orders)
        return delivery_message

        


    

