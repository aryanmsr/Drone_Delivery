
class Warehouse:

    def __init__:(self, num, x, y):
        self.num = num
        self.current_position = [x, y]
        self.products_type = []
        self.products_quantity = [] 
    
    def add_product(self, prod_type, prod_qnt):
        self.product_type.append(prod_type)
        self.products_quantity.append(prod_qnt)

    def remove_product(self, prod_type, prod_qnt):
        self.product_type.remove(prod_type)
        self.products_quantity.remove(prod_qnt)
    
