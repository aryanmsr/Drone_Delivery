# Drone_Delivery
[Final Notebook containing all of the code](https://github.com/aryanmsr/Drone_Delivery/blob/main/Notebooks/hash-code-drone-delivery.ipynb)

## Problem understanding
The Internet has profoundly changed the way we buy things, but the online shopping of today is likely not the end of that change; after each purchase we still need to wait multiple days for physical goods to be carried to our doorstep. This is where drones come in ­ autonomous, electric vehicles delivering online purchases. Flying, so never stuck in traffic. As drone technology improves every year, there remains a major issue: how do we manage and coordinate all those drones?

## Task
Given a hypothetical fleet of drones, a list of customer orders and availability of the individual products in warehouses, the task is to schedule the drone operations so that the orders are completed as soon as possible.

Description of output variables (defined according to the Hashcode instructions "File Format"):

grid_row, int, - number of rows in the grid
grid_col, int, - number of columns in the grid
n_drones, int, - number of drones available
max_turns, int, - maximum length of the simulation in "turns"
max_payload, int, - maximum load that a drone can carry

n_prod_types, int, P - total number of different product types available in wharehouses

weight_prod_types, int - list of len P, weight of each of the different product types.
n_wrhs, int, - total number of warehouses

wrhs_info, int list of len n_whrs, - each element [whrs_loc, num_itms_per_prodtype] of the array contains the location of the warehouse and the number of items of each product type in the warehouse.

Example: the first warehouse wrhs_info[0] = [[113, 179], [0, 0, 5, 1, 0, 0, 0, 0, 2, 0, 4, 0, 0, 0, 0, 8, 11, 5, 0, ...]]

n_orders, int, - total of number of order to be completed.

order_info, int - list of len n_orders, each element [order_loc, n_order_items, prod_type_of_prod_item] of the array contains the location of the order, the number of order product items and finally the the product types of the product items.

Example: the first order order_info[0] = [[340, 371], [8], [226, 183, 6, 220, 299, 280, 12, 42]]

## General approach
The main idea of our algorithm is the following: 
<ol>
  <li>Each drone finds the nearest warehouse and goes there.</li>
  <li>Next, the drone finds the nearest order whose products are available at the current warehouse and gets assigned to that order</li> 
  <li>The drone takes the products available at the warehouse and if it has some spare space ('remainder') it looks for another nearest warehouse with the products needed for the current order. If there's such a warehouse then the drone goes there to pick up the missing products types </li>
  <li>The drone delivers the order (the order may be still incomplete) and again looks for the nearest warehouse</li>
</ol>

## Some Visuals

<figure class="half">
  <table>
    <tr>
      <td>
        <img src="https://github.com/aryanmsr/Drone_Delivery/blob/main/Screen%20Shot%202022-01-13%20at%2012.16.45%20AM.png" alt="fig1" width = 500>
      </td>
      <td>
        <img src="https://github.com/aryanmsr/Drone_Delivery/blob/main/Screen%20Shot%202022-01-13%20at%2012.17.04%20AM.png" alt="fig2" width = 500>
      </td>
    </tr>
  </table>
  <figcaption>Plots visualizing drones and orders.</figcaption>
</figure>





