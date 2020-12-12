from classes.dataframes import *
from eda.input_data_sorter import *
from classes.drone import *
from classes.warehouses import *
from classes.utility import *
from classes.order import *

import time
# initialize raw data
raw_data = sort_data("./eda/busy_day.in")
grid_row, grid_col, n_drones, max_turns, max_payload, n_prod_types, weight_prod_types, n_wrhs, wrhs_info, n_orders, order_info = [
    raw_data[i] for i in range(11)]

# DRONES
drones = [Drone(i, weight_prod_types) for i in range(n_drones)]
dronesdict = dict(enumerate(drones))

# ORDERS
# n_orders =100
orderslist = [Order(i, order_info[i][0][0], order_info[i][0][1], order_info[i][1], order_info[i][2], weight_prod_types) for
          i in range(n_orders)]
ordersdict = dict(enumerate(orderslist))
orders = Orders(n_orders, ordersdict)

# WAREHOUSES
wrhslist = [Warehouse(i, wrhs_info[i][0][0], wrhs_info[i][0][1], wrhs_info[i][1], weight_prod_types) for i in
        range(n_wrhs)]
wrhsdict = dict(enumerate(wrhslist))
warehouses = Warehouses(n_wrhs, orders, wrhsdict)

# Drones must start a wharehouse 0
# then move 3 drones to each warehouse
for i in dronesdict:
    dronesdict[i].update_cur_pos(wrhsdict[0].position)
    dronesdict[i].turns += np.int(np.ceil(dist(dronesdict[i].cur_pos, wrhsdict[i % 10].position)))
    dronesdict[i].update_cur_pos(wrhsdict[i%10].position)

# do one cycle of sim:
completed = 0
message = 0
no_type = 0
total_message = []

while completed<1251:
    for k in dronesdict:
    # for k in range(2):
        # find nearest order
        # w = k%10

        drone = dronesdict[k]
        nearest_warehouse = drone.find_nearest_wh(warehouses)
        drone.turns += np.int(np.ceil(dist(drone.cur_pos, nearest_warehouse.position)))
        drone.update_cur_pos(nearest_warehouse.position)
        # if nearest_warehouse.amounts.sum()==0:
            
        nearest_warehouse.update_availability(warehouses, orders)
        nearest_order, all = drone.find_nearest_order(orders, warehouses, nearest_warehouse)
        if nearest_order == 'All orders are completed':
            message = 'DONE'
            break
        types, qnty, loading_message = drone.assign_order(nearest_order, nearest_warehouse, warehouses)
    nearest_warehouse.update_availability(warehouses, orders)

    #####
    if drone.remainder != 0:
        leftover_types = nearest_order.typelist[~np.isin(nearest_order.typelist, types)]  # qnty problem
        print(leftover_types)
        if ((len(leftover_types > 0)) and (np.any(drone.weights[leftover_types]) <= drone.remainder)):
            # if np.any(drone.weights[leftover_types])<=drone.remainder:
            wh_next_pickup, types_in_remainder = drone.find_nearest_wh_with_types(warehouses, leftover_types)
            wh_next_pickup.update_availability(warehouses, orders)  # ? probably not necessary
            # print(types_in_remainder)
            if len(types_in_remainder) > 0:
                types_in_remainder, qnty_remainder, loading_message_r = drone.assign_pickup(wh_next_pickup,
                                                                                            types_in_remainder,
                                                                                            warehouses)
                drone.turns += np.int(np.ceil(dist(drone.cur_pos, wh_next_pickup.position)))

                # update quantitites and types
                old_stack = np.column_stack((types, qnty))
                new_stack = np.column_stack((types_in_remainder, qnty_remainder))
                tot_stack = np.vstack((old_stack, new_stack))
                types, qnty = np.unique(tot_stack[:, 0], return_counts=True)
                # #sorted_stack = tot_stack[tot_stack[:,0].argsort()]
                # types = tot_stack[:,0]
                # qnty = tot_stack[:,1]
                loading_message = loading_message + loading_message_r
                print(tot_stack)

    #reset remainder done in assing_order

        if types.shape[0]>0:
            # print(nearest_order)
        # check availability of each product type order in warehouse
            delivery_message = drone.deliver_order(types, qnty, nearest_order, orders)
            max_turns_drones = np.max(np.array([x.turns for x in drones]))
            turns_orders_completed = np.array(orders.turn_order_completed)
            score = np.int(np.sum(np.ceil((max_turns_drones-turns_orders_completed)/max_turns_drones*100)))
            print(f'drone: {drone.num}, wrhs: {nearest_warehouse.num}, all: {all},\
                tot_items: {warehouses.tot_amounts}, completed: {orders.completed.sum()},\
                     items moved: {qnty.sum()}, score: {score}')

            # print(f'qnty: {qnty}, types: {types}, avail_items: {nearest_warehouse.prod_amounts.loc[types]}, items moved: {qnty.sum()}')
            total_message.append(loading_message + delivery_message)
            # nearest_warehouse.update_availability(warehouses, orders, all)
        else: 
            print('no_type')
            no_type += 1
            # if np.random.rand(1)>0.5:
            drone.update_cur_pos(nearest_order.position)
            drone.turns += np.int(np.ceil(dist(drone.cur_pos, nearest_order.position)))

            # nearest_warehouse.update_availability(warehouses, orders)
            # else:
            #     w_pos = warehouses.positions
            #     np.random.shuffle(w_pos)
            #     drone.update_cur_pos(w_pos[0])
        completed = orders.completed.sum()
    if message == 'DONE':
        print(f'orders: {orders.dict}')
        print(f'warehouses: {warehouses.dict}')
        print(f'drones: {drones}')
        print(f'message: {total_message}')
        max_turns_drones = np.max(np.array([x.turns for x in drones]))
        print(f'max number of turns: {max_turns_drones}') 
        print(f'number of cycles with 0 products delivered: {no_type}')
        turns_orders_completed = np.array(orders.turn_order_completed)
        score = np.sum(np.ceil((max_turns_drones-turns_orders_completed)/max_turns_drones*100))
        print(f'score: {score}')
        break

