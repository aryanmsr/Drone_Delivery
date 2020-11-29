from eda.input_data_sorter import *
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from classes.dataframes import *

sns.set()

data = sort_data("busy_day.in")
grid_row, grid_col, n_drones, max_turns, max_payload, n_prod_types, weight_prod_types, n_wrhs, wrhs_info, n_orders, order_info = [data[i] for i in range(11)]

#-- Geograhical plot of warehouses and orders
wrhs_loc = [wrhs_info[i][0] for i in range(len(wrhs_info))]
order_loc = [order_info[i][0] for i in range(len(order_info))]

plt.figure()
plt.title("Location of warehouses")
for i in wrhs_loc:
    plt.plot(i[0], int(i[1]), "-o")
plt.show()

plt.figure()
plt.title("Location of orders")
for i in order_loc:
    plt.plot(i[0], int(i[1]), "-x")
plt.show()

#-- Number of items in each warehouse
wrhs_n_items = [sum(i[1]) for i in wrhs_info]

plt.figure()
plt.title("Number of Items in each warehouse")
plt.bar(range(len(wrhs_info)), wrhs_n_items)
plt.show()

#-- Dataframe for the Orders [Row Location, Col Location, N of items per order]
x_order_loc = [order_info[i][0][0] for i in range(len(order_info))]
y_order_loc = [order_info[i][0][1] for i in range(len(order_info))]
n_items_per_order = [order_info[i][1][0] for i in range(len(order_info))]
df1_orders = pd.DataFrame(list(zip(x_order_loc,y_order_loc,n_items_per_order)), columns = ["X", "Y", "N of Items"])

#-- Dataframe for order Items [order N, product type, loc x, loc y]
for i in range(0, len(order_info)):
    order = [i] * len(order_info[i][2])
    prod_types_order = order_info[i][2]
    xloc = [order_info[i][0][0]] * len(order_info[i][2])
    yloc = [order_info[i][0][1]] * len(order_info[i][2])
    array = np.transpose(np.array([order, prod_types_order, xloc, yloc]))
    if i==0:
        df2 = pd.DataFrame(array, columns=["Order Number", "Product Type", "X", "Y"])
    else:
        subdf = pd.DataFrame(array, columns = ["Order Number", "Product Type", "X", "Y"])
        df2 = df2.append(subdf)

#df2.to_csv(r'/Users/FCRA/Desktop/df2.csv', index = False, header=True)                                             #Insert the path where you want to export the dataframe

#print(pd.value_counts(df2["Product Type"]))                     #number of items per product type - print format

plt.figure()
sns.set(rc = {'figure.figsize':(11.7, 8.27)})                    #number of items per product type - plot format
sns.displot(df2["Product Type"], bins=[i for i in range(n_prod_types)])
plt.title("Number of Items per Product Type in all Orders")
plt.show()

# -- Dataframe for Warehouses

data = Dataframes()
df_wrhs = data.get_df_wareouses()
print(df_wrhs)
