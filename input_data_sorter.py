
#This file sorts the data given in "busy_day.in.

#Description of output variables (defined according to the Hashcode instructions "File Format"):
# - grid_row, int, number of rows in the grid
# - grid_col, int, number of columns in the grid
# - n_drones, int, D number of drones available
# - max_turns, int, maximum length of the simulation in "turns"
# - max_payload, int, maximum load that a drone can carry
#
# - n_prod_types, int, P total number of different product types available in wharehouses
# - weight_prod_types, int list of len P, weight of each of the different product types.
# - n_wrhs, int, total number of warehouses
#
# - wrhs_info, int list of len n_whrs, each element [whrs_loc, num_itms_per_prodtype] of the array contains the location of the warehouse and the number of items of each product type in the warehouse.
#                                   Example: the first warehouse
#                                   wrhs_info[0] = [[113, 179], [0, 0, 5, 1, 0, 0, 0, 0, 2, 0, 4, 0, 0, 0, 0, 8, 11, 5, 0, ...]]
#
# - n_orders, int, total of number of order to be completed.
# - order_info, int list of len n_orders, each element [order_loc, n_order_items, prod_type_of_prod_item] of the array contains the location of the order, the number of order product items and finally the the product types of the product items.
#                                   Example: the first order
#                                   order_info[0] = [[340, 371], [8], [226, 183, 6, 220, 299, 280, 12, 42]]
#

def sort_data(text):
        f = open(text, "r")
        lines = f.readlines()
        f.close()

        grid_row, grid_col, n_drones, max_turns, max_payload = [int(lines[0].split()[i]) for i in range(5)]
        n_prod_types = int(lines[1])
        weight_prod_types = lines[2].split()
        weight_prod_types = [int(i) for i in weight_prod_types]         #making elements int
        n_wrhs = int(lines[3])

        wrhs_info = []
        i=4
        while(i<n_wrhs*2+4):
            wrhs_loc, num_itms_per_prodtype = lines[i].split(), lines[i+1].split()
            wrhs_loc = [int(i) for i in wrhs_loc]
            num_itms_per_prodtype = [int(i) for i in num_itms_per_prodtype]
            wrhs_info.append([wrhs_loc, num_itms_per_prodtype])
            i = i+2

        n_orders = int(lines[24])
        i=25
        order_info = []
        while(i<n_orders*3+25):
            order_loc, n_order_items, prod_type_of_prod_item =  lines[i].split(), lines[i+1].split(), lines[i+2].split()
            order_loc = [int(i) for i in order_loc]
            n_order_items = [int(i) for i in n_order_items]
            prod_type_of_prod_item = [int(i) for i in prod_type_of_prod_item]
            order_info.append([order_loc, n_order_items, prod_type_of_prod_item])
            i = i+3
        return grid_row, grid_col, n_drones, max_turns, max_payload, n_prod_types, weight_prod_types, n_wrhs, wrhs_info, n_orders, order_info

