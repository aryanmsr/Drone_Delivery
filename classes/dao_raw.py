from eda.input_data_sorter import sort_data


class Dao:
    data = sort_data("./eda/busy_day.in")
    grid_row, grid_col, n_drones, max_turns, max_payload, n_prod_types, weight_prod_types, n_wrhs, wrhs_info, n_orders, order_info = [
        data[i] for i in range(11)]

    # get the location based on order types
