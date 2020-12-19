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
    # dronesdict[i].turns += np.int(np.ceil(dist(dronesdict[i].cur_pos, wrhsdict[i % 10].position)))
    dronesdict[i].update_cur_pos(wrhsdict[i%10].position)

# do one cycle of sim:
completed = 0
message = 0
no_type = 0
remainder = 0
total_message = []

while completed<1251:
    loading_message_r = []
    drone_turns = np.array([x.turns for x in dronesdict.values()])
    drone = dronesdict[np.argmin(drone_turns)]
    nearest_warehouse = drone.find_nearest_wh(warehouses)
    drone.update_cur_pos(nearest_warehouse.position)
        
    nearest_warehouse.update_availability(warehouses, orders)
    nearest_order, all = drone.find_nearest_order(orders, warehouses, nearest_warehouse)
    if nearest_order == 'All orders are completed':
        message = 'DONE'
        break
    types, qnty, loading_message, nono = drone.assign_order(nearest_order, nearest_warehouse, warehouses, orders)
    nearest_warehouse.update_availability(warehouses, orders)
    if types.shape[0]>0:
    # check availability of each product type order in warehouse
        delivery_message = drone.deliver_order(types, qnty, nearest_order, orders)
        # print(f'drone: {drone.num}', f'wrhs: {nearest_warehouse.num}',f'all: {all}',
        # f'tot_items: {warehouses.tot_amounts}', f'completed: {orders.completed.sum()}',
        #             f'items moved: {qnty.sum()}', f'remainder: {remainder}', sep = ',')
        print(f'completed : {orders.completed.sum()}')
        # if loading_message_r !=[]:
        #     print(f'load: {loading_message}', f'load_r: {loading_message_r}', 
        #     f'delivery: {delivery_message}')
        # total_message.append(loading_message + delivery_message)
        if len(nono)>0:
            types_nono, qnty_nono, order_nono = nono
            # print(nearest_order, order_nono)
            delivery_message_nono = drone.deliver_order(types_nono, qnty_nono, order_nono, orders)
            delivery_message += delivery_message_nono
        total_message.append(loading_message + delivery_message)
        assert len(loading_message) == len(delivery_message)
    else: 
        print('no_type')
        no_type += 1
    completed = orders.completed.sum()
if message == 'DONE':
#     print(f'orders: {orders.dict}')
    print(f'warehouses: {warehouses.dict}')
#     print(f'drones: {drones}')
    final_message = []
    for x in total_message:
        final_message.extend(x)
    n_lines = len(final_message)
#     print(f'message: {total_message}')
    max_turns_drones = np.max(np.array([x.turns for x in drones]))
    print(f'max number of turns: {max_turns_drones}') 
    print(f'number of cycles with 0 products delivered: {no_type}')
    turns_orders_completed = np.array(orders.turn_order_completed)
    score = np.sum(np.ceil((max_turns_drones-turns_orders_completed)/max_turns_drones*100))
    print(f'score: {score}')
    
# pd_message = pd.concat((pd.Series(n_lines), pd.Series(final_message)), ignore_index = True)
# pd_message.to_csv('submission.csv', index = False, header = False)

