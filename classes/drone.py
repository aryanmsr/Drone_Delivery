from classes.dataframes import *
import numpy as np
from classes.utility import *
from classes.order import *
from classes.warehouses import *
import pandas as pd

class Drone():  # inherit #product #warehouse #order (#utility)

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
        self.remainder = 0

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
        # print(avail_types, avail_qnty)

        # If all order fits in the drone
        if np.sum(self.weights[avail_types]*avail_qnty)<=200: # the drone can leave the warehouse with spare space
            new_types = avail_types
            new_qnty = avail_qnty
            # wrhs.remove_product(new_types, new_qnty, warehouses)
            # self.load(new_types, new_qnty, wrhs)

        #if order is heavier than drone max payload mass
        # why would it look for another nearest warehouse? 
        else:
            # types = np.repeat(avail_types, avail_qnty)
            # weights = 
            types = np.repeat(avail_types, avail_qnty)
            weights = self.weights[types]
            repeated_matrix = np.column_stack((types, weights))
            rep_mat_sorted = repeated_matrix[repeated_matrix[:,1].argsort()]
            # x = np.median(weights)

            # heaviest = rep_mat_sorted[rep_mat_sorted[:,1]>x]
            # lightest_reverted = rep_mat_sorted[rep_mat_sorted[:,1]<=x][::-1]
            # if len(heaviest)==0:
            #     new_sorted_matrix = lightest_reverted
            # else:
            #     new_sorted_matrix = np.vstack([heaviest[0], lightest_reverted, heaviest[1:]]) 
            # mask_le200 = new_sorted_matrix[:,1].cumsum() <= 200
            new_sorted_matrix = rep_mat_sorted[::-1]
            mask_le200 = new_sorted_matrix[:,1].cumsum() <= 200
            new_types_repeated = new_sorted_matrix[mask_le200][:,0]
            # new_types_repeated = rep_mat_sorted[mask_le200][:,0]
            # new_types_repeated = repeated_matrix[repeated_matrix[repeated_matrix[:,1].argsort()][:,1].cumsum()<=200][:,0]
            new_types, new_qnty = np.unique(new_types_repeated, return_counts=True)
            new_weigths_repeated = self.weights[new_types_repeated]
            remainder = 200 - new_weigths_repeated.sum()
            # if remainder >= np.min(self.weights):
            self.remainder = remainder
            ###
            # self.remainder = 200 - new_weigths_repeated.sum()
            # leftover_types = order.typelist[~np.isin(order.typelist, types)]
            # if (leftover_types.shape[0] > 0) and np.any(self.remainder >= self.weights[leftover_types]):


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
        assert order.amount >= qnty.sum()
        delivery_message = self.deliver(types, qnty, order, orders)
        order.remove_prod(types, qnty)
        assert order.amount >= 0
        self.remainder = 0
        # order.assigned -= 1
        self.compute_weight()
        order.check_completed(self.turns, orders)
        return delivery_message

    # method necessary for reminder
    def find_nearest_wh_with_types(self, warehouses, leftover_types):
        leftover_acceptable_types = leftover_types[self.weights[leftover_types]<=self.remainder]
        avail_acceptable_leftover = np.array([np.any(x[leftover_acceptable_types]) for x in warehouses.avail_products])
        wh = np.array(warehouses.positions, dtype=np.float64)
        wh[~avail_acceptable_leftover] = np.inf
        d = dist(self.cur_pos, wh)
        if d.min() == np.inf:
            return 'no_pickup', []
        index_argmin = np.argmin(d)
        wh_next_pickup = warehouses.dict[index_argmin]
        types_in_remainder = leftover_types[wh_next_pickup.avail_products[leftover_types]]
        types_sorted = types_in_remainder[self.weights[types_in_remainder].argsort()]
        types_chosen = types_sorted[self.weights[types_sorted].cumsum()<=self.remainder]
        return wh_next_pickup, types_chosen  

    def find_nearest_wh_with_types1(self, warehouses, leftover_types):

        all_types_avail_in_whs = np.array([np.flatnonzero(i) for i in warehouses.avail_products])

        # wh_num_types_avail = []  #give priority to the ones with most product types that fit in the remainder
        wh_with_leftover_types = []  # 1, 2, 3
        wh_checked_types = []  # [50],[51, 52],[

        for i in range(len(all_types_avail_in_whs)):  # 10 iterations
            check = np.isin(leftover_types, all_types_avail_in_whs[i])
            checked_types = leftover_types[check]  ##che sono minori del reminder
            # print(checked_types)
            if len(checked_types) > 0:
                wh_with_leftover_types.append(i)
                wh_checked_types.append(checked_types)
                # mask_remainder = checked_types.cumsum() <= self.remainder
                # wh_num_types_avail.append(len(checked_types[mask_remainder]))
        # print(wh_with_leftover_types)
        wh = np.array(warehouses.positions, dtype=np.float64)

        # give priority to the ones with most product types that fit in the remainder
        # wh_priority_list = np.argsort(wh_num_types_avail)[::-1]

        # if len(wh_with_leftover_types)>0:
        wh_positions = np.array([wh[i] for i in wh_with_leftover_types])  # mask
        # [1, 4, 6]
        # [1]
        d = dist(self.cur_pos, wh_positions)
        index_argmin = np.argmin(d)

        wh_next_pickup = {k: warehouses.dict[k] for k in wh_with_leftover_types}[wh_with_leftover_types[index_argmin]]
        # else:
        #     wh_next_pickup = warehouses.dict[wh_with_leftover_types[0]]

        mask_chosen = self.weights[
                          wh_checked_types[wh_with_leftover_types.index(wh_next_pickup.num)]].cumsum() <= self.remainder
        types_in_remainder = wh_checked_types[wh_with_leftover_types.index(wh_next_pickup.num)][mask_chosen]
        # print(f'Cosa Abbiamo : {types_in_remainder}')

        return wh_next_pickup, types_in_remainder  

    def assign_pickup(self, wh_next_pickup, types_in_remainder, warehouses):
        # Quantity is just 1
        qnty_remainder = np.ones(len(types_in_remainder), dtype=np.int64)
        wh_next_pickup.remove_product(types_in_remainder, qnty_remainder, warehouses)
        loading_message = self.load(types_in_remainder, qnty_remainder, wh_next_pickup)

        assert self.compute_weight().sum() <= 200

        # print(types_in_remainder)
        # print(wh_next_pickup)
        self.remainder -= self.weights[types_in_remainder].sum()
        return types_in_remainder, qnty_remainder, loading_message
