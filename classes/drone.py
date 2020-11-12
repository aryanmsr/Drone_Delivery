# This is the drone class

class Drone():  # inherit                   #product #warehouse #order (#utility)

    def __init__(self, num):
        self.num = num
        self.products_type = []
        self.products_quantity = []
        #  self.items = []         #List[[n, pt]]
        self.pld_mass = 0
        self.cur_pos = [0, 0]
        self.turns = 0  # ?
        self.actions = []  # ?
        self.busy = False

    def load(self, prod_type, qnty):
        self.items.append([qnty, prod_type])
        # pactions.append([0 L 1 2 3 ]) ?order_number
        self.turns += 1

    def unload(self, prod_type, qnty):  # warehouse
        self.items.remove([qnty, prod_type])
        # actions.append([0 U 1 2 3 ])?order_number
        self.turns += 1

    # def unpdate_pld_mass(self):
    # for i in items:
    # weight += dao.get_weight(item)
    # pld_mass = weight

    def deliver(self, prod_type, qnty):  # to the order
        self.items.remove([qnty, prod_type])
        # actions.append([0 D 1 2 3 ])?order_number
        self.turns += 1

    def wait(self, n_turns):
        self.turns += n_turns

    def get_cur_pos(self):
        return self.cur_pos

    def update_cur_pos(self, new_pos):
        self.cur_pos = new_pos  # define in utility class

    #account for distance in the count of turns for delivery
