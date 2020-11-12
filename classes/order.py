
class Order:

    def __init__(self, num, x, y):
       self.num = num
       self.position = [x, y]
       self.product_type = []
       self.products_quantity = []
       self.completed = False
       self.turn_order_completed = 0

    def add_product(self, prod_type, prod_qnt):
        self.product_type.append(prod_type)
        self.products_quantity.append(prod_qnt)

    def remove_product(self, prod_type, prod_qnt):
        self.product_type.remove(prod_type)
        self.products_quantity.remove(prod_qnt)

