import math
from classes.dataframes import *

class Utility:

    def __init__(self):
        self.Data = Dataframes()
        self.df_orders = self.Data.get_df_orders()
        self.grid_rows = self.Data.grid_row
        self.grid_cols = self.Data.grid_col

    def calc_distance(self, xa, ya, xb, yb):
        return math.sqrt((abs(xa - xb)) ** 2 + (abs(ya - yb)) ** 2)

    def num_turns(self, dist):
        return math.ceil(dist)

    # get closest order location and distance to current drone position
    def min_distance(self, cur_pos):
        min = math.sqrt(self.grid_rows ** 2 + self.grid_cols ** 2)
        x_pos, y_pos = 0, 0
        for index, row in self.df_orders.iterrows():
            tmp = self.calc_distance(cur_pos[0], cur_pos[1], row["X"], row["Y"])
            if tmp < min:
                min = tmp
                x_pos = row["X"]
                y_pos = row["Y"]
        return [min, x_pos, y_pos]


    # def find_new_pos(self, xa, ya, xb, yb):
