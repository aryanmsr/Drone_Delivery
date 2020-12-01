from classes.dataframes import *
import numpy as np
from classes.utility import *


class Drone(object):  # inherit #product #warehouse #order (#utility)

    def __init__(self, num):
        self.num = num
        self.prod_types = []
        self.prod_amounts = []
        self.pld_mass = 0
        self.cur_pos = [0, 0]
        self.turns = 0  # ?
        self.actions = []  # ?
        self.busy = False

        # Df for use throughout
        self.Data = Dataframes()
        # self.Util = Utility()

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'payload_weight: ' + str(sum(self.prod_types)) + ')'

    def load(self, prod_types, qnty):
        self.prod_types.append(prod_types)
        self.prod_amounts.append(qnty)
        # pactions.append([0 L 1 2 3 ]) ?order_number
        self.turns += 1
        # TODO update payload mass

    def unload(self, prod_types, qnty):  # warehouse
        self.prod_types.remove(prod_types)
        self.prod_amounts.remove(qnty)
        # actions.append([0 U 1 2 3 ])?order_number
        self.turns += 1

    def unpdate_pld_mass(self):
        tot_weight = 0
        for i in range(len(self.prod_types)):
            unit_weight = self.Data.weight_prod_types[self.prod_types[i]]
            tot_weight += unit_weight * self.prod_amounts[i]
        self.pld_mass = tot_weight

    def deliver(self, prod_type, qnty):  # to the order
        self.prod_types.remove(prod_type)
        self.prod_amounts.remove(qnty)
        # actions.append([0 D 1 2 3 ])?order_number
        self.turns += 1

    def wait(self, n_turns):
        self.turns += n_turns

    def get_cur_pos(self):
        return self.cur_pos

    def update_cur_pos(self, new_pos):
        self.cur_pos = new_pos  # define in utility class

    # account for distance in the count of turns for delivery

    def find_nearest_wh(self, warehouses):
        wh = np.array([warehouses[x].position for x in warehouses], dtype=np.float64)
        d = dist(self.cur_pos, wh)
        return warehouses[np.argmin(d)]

    def check_pld_weight(self):
        return self.pld_mass <= 200
