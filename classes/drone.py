# This is the drone class

class Drone:

    def __init__(self, num):
        self.num
        self.products_type = [] # add to Francesca's notebook
        self.products_quantity = [] # list of lists  
        self.payload_mass = 0
        self.current_position = []
        self.turns = 0
        self.actions = []

    def load(self, products_type, products_quantity):
        self.products_type.append(products_type)
        self.products_quantity.append(products_quantity)

    def unload(self, products_type, products_quantity):
        self.products_type.remove(products_type)
        self.products_quantity.remove(products_quantity)
       
    
    def deliver(self):

    def wait(self):

    def current_position(self):

