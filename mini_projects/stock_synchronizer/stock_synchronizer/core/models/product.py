class Product:

    def __init__(self, id, parent_id, stock):
        self.id = id
        self.stock = stock
        self.parent_id = parent_id
        self.children_ids = []
        self.is_active = True

    def update_stock(self, new_stock):
        self.stock = new_stock

    def deactivate(self):
        self.is_active = False
