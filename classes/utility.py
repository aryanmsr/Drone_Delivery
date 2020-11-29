import math
from classes.dataframes import *
import numpy as np


# class Utility:
#
#     def __init__(self):
#         self.Data = Dataframes()
#         self.df_orders = self.Data.get_df_orders()
#         self.grid_rows = self.Data.grid_row
#         self.grid_cols = self.Data.grid_col
#         self.df_wrhs = self.Data.get_df_wareouses()

# def calc_distance(self, xa, ya, xb, yb):
#     return math.sqrt((abs(xa - xb)) ** 2 + (abs(ya - yb)) ** 2)

def dist(a, b):
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.sqrt(((a - b) ** 2).sum(1))
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def num_turns(self, dist):
    return math.ceil(dist)

    # get closest order location and distance to current drone position
    # def get_closest_order(self, cur_pos):
    #     min = math.sqrt(self.grid_rows ** 2 + self.grid_cols ** 2)
    #     x_pos, y_pos = 0, 0
    #     for index, row in self.df_orders.iterrows():
    #         tmp = self.calc_distance(cur_pos[0], cur_pos[1], row["X"], row["Y"])
    #         if tmp < min:
    #             min = tmp
    #             x_pos = row["X"]
    #             y_pos = row["Y"]
    #     return [min, x_pos, y_pos]
    #
    #
    # def get_closest_warehouse(self, cur_pos):
    #     min = math.sqrt(self.grid_rows ** 2 + self.grid_cols ** 2)
    #     x_pos, y_pos = 0, 0
    #     for index, row in self.df_wrhs.iterrows():
    #         tmp = self.calc_distance(cur_pos[0], cur_pos[1], row["X"], row["Y"])
    #         if tmp < min:
    #             min = tmp
    #             x_pos = row["X"]
    #             y_pos = row["Y"]
    #     return [min, x_pos, y_pos]






    # def find_new_pos(self, xa, ya, xb, yb):
