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
