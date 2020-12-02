import numpy as np
import pandas as pd
import collections


class Order(object):

    def __init__(self, num, x, y, amount, types, weight_prod_types):
        # x - location
        # y - location
        # amount - total number of items
        # types - [1, 1, 2, 3 4, 4]
        # weight product types - initialized @ beginning of sim

        self.amount = amount
        self.num = num
        self.position = [x, y]
        self.completed = False
        self.turn_order_completed = 0

        self.weights = np.array(weight_prod_types)
        self.tot_weight = self.weights[types].sum()

        self.prod_types = np.array(types)
        self.prod_amounts = pd.DataFrame(np.unique(self.prod_types, return_counts=True)).T.rename(
            columns={0: "Types", 1: "Amounts"})

        # -- Other methods we could have used
        # = collections.Counter(self.prod_types
        # pd.Series(self.prod_types).value_counts()            #number of items per product type
        # self.products_quantity = pd.Series(self.products_type, columns = 'type').groupby('type').count()
        # self.prod_weights = weights[types]

    def __repr__(self):
        return '(num: ' + str(self.num) + ', ' + 'n_items: ' + str(
            self.amount) + ', ' + 'tot_weight: ' + str(self.tot_weight) + ')'

    # TODO: improve remove method, but watch out because it's used in main_sim
    def remove_prod(self, prod_type, prod_qnt):
        # self.prod_type.remove(prod_type), should be sufficient to simply undate the quantities
        self.prod_amounts.iloc[prod_type]["Amounts"] = 0

    def check_completed(self):
        return self.prod_amounts["Amounts"].sum == 0



# ord = Order(1, 23, 34, 5, [1, 1, 2, 3, 4], [1, 1, 1, 1, 1])
# print(ord.prod_amounts)
# print(ord.prod_amounts.loc[ord.prod_amounts["Types"]==1]["Amounts"])
