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

# assign each drone to a warehouse
# for k in dronesdict.keys():
#     dronesdict[k].update_cur_pos(wrhsdict[k].position)
for i in dronesdict:
    dronesdict[i].update_cur_pos(wrhsdict[0].position)
# do one cycle of sim:
# each drone at each warehouse

# while t<=max_turns:
while orders.completed.sum()<100:
    for k in dronesdict:
    # for k in range(2):
        # find nearest order
        w = k%10
        # t = time.time()
        drone = dronesdict[k]
        nearest_warehouse = drone.find_nearest_wh(wrhsdict)
        drone.turns += np.ceil(dist(drone.cur_pos, nearest_warehouse.position))
        drone.update_cur_pos(nearest_warehouse.position)
        # t1 = time.time()
        # print(f'nearest_wh: {t1-t}')
        nearest_order = drone.find_nearest_order(orders, warehouses, nearest_warehouse)
        types, qnty = drone.assign_order(nearest_order, nearest_warehouse, warehouses)
        t2 = time.time()
        # print(f'nearest_order: {t2-t1}')
        # check availability of each product type order in warehouse
        nearest_warehouse.update_availability(warehouses, orders)
        t3 = time.time()
        print(f'assign: {t3-t2}')
        drone.deliver_order(types, qnty, nearest_order, orders)
        # t4 = time.time()
        # print(f'deliver: {t4-t3}')
        # print(orders.completed.sum())
        # print(drone.turns)
        print(orders.completed.sum())
        # print(nearest_warehouse.prod_amounts.Amounts.sum(), nearest_warehouse.num)
    # avail_types = wrhsdict[k].select_avail_types(nearest_order.prod_types)
    # print(avail_types)
    # avail_qnty = wrhsdict[k].select_avail_quantities(avail_types, nearest_order.df.loc[avail_types])
    # print(avail_qnty)
    # print(wrhsdict[k].prod_amounts.loc[nearest_order.prod_types])

    # wrhsdict[k].remove_product(avail_types, avail_qnty)

    # print(wrhsdict[k].prod_amounts.loc[nearest_order.prod_types])



    # print(wrhsdict[k].prod_amounts[wrhsdict[k].prod_amounts['Amounts']>0])



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
