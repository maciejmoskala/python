from stock_synchronizer.core.models.product import Product
from stock_synchronizer.core.output_event import JsonOutputEvent
from stock_synchronizer.event_sourcing.publisher import EventPublisher


class ProductHandler:

    def __init__(self):
        self.products = {}
        self.changed_products = []
        self.Publisher = EventPublisher()

    def create_product(self, id, parent_id, stock):
        product = Product(id, parent_id, stock)

        if id in self.products:
            raise Exception('Product already exists! {}'.format(self.products))

        if parent_id is not None:
            try:
                parent_product = self.products[parent_id]
                parent_product.children_ids.append(id)
            except Exception:
                raise Exception('Unknown parent product!')

        self.products[id] = product

    def update_product(self, id, stock):
        self.changed_products = [id]

        product = self.products[id]
        product.update_stock(stock)

        self._update_parent_product(product.parent_id, stock)
        self._update_children_products(product.children_ids, stock)

    def end_product(self, id):
        product = self.products[id]
        product.deactivate()

        self._end_children_products(product.children_ids)

    def summary(self):
        self._send_output_message('StockSummary')

    def clean_products(self):
        self.products = {}

    def _update_parent_product(self, parent_id, stock):
        if parent_id is None:
            return

        if parent_id in self.changed_products:
            return

        self._update_product(parent_id, stock)

    def _update_children_products(self, children_ids, stock):
        if not children_ids:
            return

        for id in children_ids:
            if id in self.changed_products:
                continue
            self._update_product(id, stock)

    def _update_product(self, id, stock):
        product = self.products[id]
        if stock == 0:
            product.deactivate()
            self._send_output_message('EndProduct', id)
        else:
            product.update_stock(stock)
            self._send_output_message('UpdateProduct', id)
        self.changed_products.append(id)

        self._update_parent_product(product.parent_id, stock)
        self._update_children_products(product.children_ids, stock)

    def _end_children_products(self, children_ids):
        if not children_ids:
            return

        for id in children_ids:
            product = self.products[id]
            product.deactivate()
            self._send_output_message('EndProduct', id)

            self._end_children_products(product.children_ids)

    def _send_output_message(self, message_type, id=None):
        if message_type == 'UpdateProduct':
            messgae_params = {
                'id': id,
                'stock': self.products[id].stock,
            }
        elif message_type == 'EndProduct':
            messgae_params = {
                'id': id,
            }
        elif message_type == 'StockSummary':
            messgae_params = {
                'stocks': {k: v.stock for k, v in self.products.items()},
            }
        else:
            raise Exception('Unknown message type')

        event = JsonOutputEvent(message_type, **messgae_params)
        message = event.to_json()
        self.Publisher.publish(message)
