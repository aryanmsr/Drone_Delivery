from eda.input_data_sorter import sort_data
import pandas as pd


class Dataframes(object):

    def __init__(self):
        data = sort_data("./eda/busy_day.in")
        self.grid_row, \
        self.grid_col, \
        self.n_drones, \
        self.max_turns, \
        self.max_payload, \
        self.n_prod_types, \
        self.weight_prod_types, \
        self.n_wrhs, \
        self.wrhs_info, \
        self.n_orders, \
        self.order_info = [data[i] for i in range(11)]

    def get_df_orders(self):
        x_order_loc = [self.order_info[i][0][0] for i in range(len(self.order_info))]
        y_order_loc = [self.order_info[i][0][1] for i in range(len(self.order_info))]
        n_items_per_order = [self.order_info[i][1][0] for i in range(len(self.order_info))]
        df_orders = pd.DataFrame(list(zip(x_order_loc, y_order_loc, n_items_per_order)),
                                 columns=["X", "Y", "N of Items"])
        return df_orders

    def get_df_wrhs(self):
        wrhs_x = [self.wrhs_info[i][0][0] for i in range(len(self.wrhs_info))]
        wrhs_y = [self.wrhs_info[i][0][1] for i in range(len(self.wrhs_info))]
        n_items_per_product_type = [self.wrhs_info[i][1] for i in range(len(self.wrhs_info))]
        df_wrhs = pd.DataFrame(list(zip(wrhs_x, wrhs_y, n_items_per_product_type)),
                               columns=["X", "Y", "Amounts"])
        return df_wrhs

# 0 0 0 0 0 0 0


    # get the location based on order types
