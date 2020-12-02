from classes.dataframes import *
from eda.input_data_sorter import *
from classes.drone import *
from classes.warehouses import *
from classes.utility import *
from classes.order import *

# initialize raw data
raw_data = sort_data("../eda/busy_day.in")
grid_row, grid_col, n_drones, max_turns, max_payload, n_prod_types, weight_prod_types, n_wrhs, wrhs_info, n_orders, order_info = [
    raw_data[i] for i in range(11)]

# For now: override n_drones with n_whrs, so we have 1 drone per whrs
n_drones = n_wrhs

# initialize dfs
# data = Dataframes()
# df_orders = data.get_df_orders()
# df_wrhs = data.get_df_wrhs()

# DRONES
drones = [Drone(i + 1) for i in range(n_drones)]
dronesdict = dict(enumerate(drones))

# WAREHOUSES
wrhs = [Warehouse(i + 1, wrhs_info[i][0][0], wrhs_info[i][0][1], wrhs_info[i][1], weight_prod_types) for i in
        range(n_wrhs)]
wrhsdict = dict(enumerate(wrhs))

# ORDERS
orders = [Order(i, order_info[i][0][0], order_info[i][0][1], order_info[i][1], order_info[i][2], weight_prod_types) for
          i in range(n_orders)]
ordersdict = dict(enumerate(orders))

# assign each drone to a warehouse
for k in dronesdict.keys():
    dronesdict[k].update_cur_pos(wrhsdict[k].position)

# do one cycle of sim:
# each drone at each warehouse
for k in dronesdict.keys():
    # find nearest order
    nearest_order = wrhsdict[k].find_nearest_order(ordersdict)
    # check availability of each product type order in warehouse
    print(nearest_order)

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
