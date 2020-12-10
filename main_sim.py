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

# For now: override n_drones with n_whrs, so we have 1 drone per whrs
# n_drones = n_wrhs

# initialize dfs
# data = Dataframes()
# df_orders = data.get_df_orders()
# df_wrhs = data.get_df_wrhs()

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

# assign each drone to warehouse 0
# for i in dronesdict:
#     dronesdict[i].update_cur_pos(wrhsdict[0].position)
    
for i in dronesdict:
    dronesdict[i].update_cur_pos(wrhsdict[i%10].position)
# do one cycle of sim:
# each drone at each warehouse
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
        if types.shape[0]>0:
            # print(nearest_order)
        # check availability of each product type order in warehouse
            delivery_message = drone.deliver_order(types, qnty, nearest_order, orders)
            print(f'drone: {drone.num}, wrhs: {nearest_warehouse.num}, all: {all}, tot_items: {warehouses.tot_amounts}, completed: {orders.completed.sum()}, items moved: {qnty.sum()}')
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
        print(f'max number of turns: {np.max(np.array([x.turns for x in drones]))}') 
        print(f'number of cycles with 0 products delivered: {no_type}')
        break

    # for i in dronesdict:
    #     dronesdict[i].update_cur_pos(wrhsdict[i%10].position)
    # avail_types = wrhsdict[k].select_avail_types(nearest_order.prod_types)
    # avail_qnty = wrhsdict[k].select_avail_quantities(avail_types, nearest_order.df.loc[avail_types])

    # wrhsdict[k].remove_product(avail_types, avail_qnty)
    #
    # for prod_type in nearest_order.prod_types:
    #
    #     # retrieve quantity from order data frame
    #     prod_qnty = nearest_order.prod_amounts.loc[nearest_order.prod_amounts["Types"] == prod_type, "Amounts"].values[0]
    #
    #     # if quantity is available
    #     if wrhsdict[k].check_avail2(prod_type, prod_qnty) == True:
    #         # load items on drone
    #         dronesdict[k].load(prod_type, prod_qnty)
    #         # remove items from whrs
    #         wrhsdict[k].remove_product(prod_type, prod_qnty)
    #     # else:
    #     # print("ORDER " + nearest_order.num + ": Product Type '" + prod_type + "' is not available in quantity " + prod_qnty + ".")
    #
    # # fly to order
    # dronesdict[k].update_cur_pos(nearest_order.position)
    # # unload the product items onboard and remove from order list.
    # for i in range(len(dronesdict[k].prod_types)):
    #     prod_type = dronesdict[k].prod_types[i]
    #     prod_qnty = dronesdict[k].prod_amounts[i]
    #     # unload
    #     dronesdict[k].unload(prod_type, prod_qnty)
    #     # remove delivered items from the order
    #     nearest_order.remove(prod_type, prod_qnty)  # TODO fix error
    #
    # nearest_order.check_completed()

# TODO: check that the nearest orders found are not the same for each drone
# TODO: check for maximum payload mass
# TODO: deal with unavailable quantities


# nearest_wrhs = v.find_nearest_wh(wrhsdict)
# Drones
# for warehouse class
# for order class
