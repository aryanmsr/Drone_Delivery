import numpy as np
import pandas as pd
from classes.utility import *


class Warehouse(object):

    def __init__(self, num, x, y, amounts, weight_product_types):
        # amounts - list of every product type amount, some are zero if that product type is not available
        # weight_product_types - weights of product types in this warehouse
        self.num = num
        self.position = [x, y]

        # self.prod_type =
        self.prod_amounts = pd.DataFrame({"Amounts": amounts, "Weights": weight_product_types})

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'position: ' + str(self.position) + ')'

    # Useless?
    def add_product(self, prod_type, prod_qnt):
        self.prod_amounts.append(prod_qnt)

    # TODO: improve this method
    # update number of items of the product type that is removed
    def remove_product(self, prod_type, prod_qnt):
        self.prod_amounts.loc[prod_type, "Amounts"] -= prod_qnt

    #
    def find_nearest_order(self, orders):  # dictionary of orders
        o = np.array([orders[x].position for x in orders], dtype=np.float64)

        c = np.array([orders[x].completed for x in orders])
        check_avail = np.array([np.any(self.check_avail(orders[x].prod_types)) for x in orders])

        if c.sum() == 1250:
            return 'All orders are completed'
        # set distances to infinity of completed orders and orders not available
        o[c] = np.inf
        o[~check_avail] = np.inf

        d = dist(self.position, o)

        # w = dist(self.position, o.warehouses)
        return orders[np.argmin(d)]

    # TODO consider integrating this check in find_nearest_order
    def check_avail(self, prod_types):  # prod_types  , prod_qnty
        # checking for the type
        return pd.Series(prod_types).isin(self.prod_amounts[self.prod_amounts["Amounts"] > 0].index)

    # check product availability only based on quantity
    def check_avail2(self, prod_type, prod_qnty):
        # checking for the quantity
        return self.prod_amounts.loc[self.prod_amounts.index == prod_type, "Amounts"].values[0] >= prod_qnty

# wrh = Warehouse(1, 23, 34, [5, 6, 82, 3, 0], [10, 11, 22, 33, 44])
# wrh.remove_product(2, 10)
# print(wrh.prod_amounts)
# print(wrh.check_avail2(0, 4))
# print(wrh.check_avail2(0, 5))
# print(wrh.check_avail2(0, 6))
