import math


class Utility:

    def calc_distance(self, xa, ya, xb, yb):
        return math.sqrt(abs(xa - xb) ** 2 + abs(ya - yb) ** 2)

    def num_turns(self, dist):
        return math.ceil(dist)

    # def find_new_pos(self, xa, ya, xb, yb):

    # give a minimum distance from the drone to any order
    def min_distance(self, orders, cur_pos):
        #        for i in orders:
        #            min = math.sqrt(n_rows ** 2 + n_cols ** 2)
        #            tmp = self.calc_distance(cur_pos[0], cur_pos[1], orders[i][0], orders[i][1])
        #            if tmp < min:
        #                min = tmp
        return min

    #
