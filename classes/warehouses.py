import numpy as np
from classes.utility import *

class Warehouse:

    def __init__(self, num, x, y, amounts, weight_product_types):
        # amounts - list of every product type amount, some are zero if that product type is not available
        # weight_product_types - weights of product types in this warehouse
        self.num = num
        self.position = [x, y]

        # self.prod_type =
        self.prod_amounts = pd.DataFrame({"Amounts": amounts, "Weights": weight_product_types})
    
    def add_product(self, prod_type, prod_qnt):
        self.prod_amounts.append(prod_qnt)

    # update number of items of the product type that is removed
    def remove_product(self, prod_type, prod_qnt):
        self.prod_amounts.loc[prod_type, "Amounts"] -= prod_qnt

    def find_nearest_order(self, orders):  # dictionary of orders
        o = np.array([orders[x].position for x in orders], dtype=np.float64)
        c = np.array([orders[x].completed for x in orders])
        if c.sum() == 1250:
            return 'All orders are completed'
        o[c] = np.inf
        d = dist(self.cur_pos, o)

        # w = dist(self.cur_pos, o.warehouses)
        return orders[np.argmin(d)]


wrh = Warehouse(1, 23, 34, [5, 6, 82, 3, 0], [10, 11, 22, 33, 44])
wrh.remove_product(2, 10)
print(wrh.prod_amounts)
