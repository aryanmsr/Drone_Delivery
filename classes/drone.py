# This is the drone class

class Drone:

    def __init__(self, num):
        self.num = num
        self.orders = []
        self.items = []
        self.payload_mass = 0

    def load(self, item):
        self.items.append(item)

    def unload(self, item):
        self.items.remove(item)
