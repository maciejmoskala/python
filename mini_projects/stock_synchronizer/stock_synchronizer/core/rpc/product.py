from stock_synchronizer.core.handlers.product_handler import ProductHandler

PRODUCT_HANDLER = ProductHandler()


def ProductCreated(**params):
    id = params.get('id')
    parent_id = params.get('parent_id')
    stock = params.get('stock')
    if any(element is None for element in (id, stock)):
        raise Exception('Incorrect event structure')

    PRODUCT_HANDLER.create_product(id, parent_id, stock)


def ProductUpdated(**params):
    id = params.get('id')
    stock = params.get('stock')
    if any(element is None for element in (id, stock)):
        raise Exception('Incorrect event structure')

    PRODUCT_HANDLER.update_product(id, stock)


def ProductEnded(**params):
    id = params.get('id')
    if id is None:
        raise Exception('Incorrect event structure')

    PRODUCT_HANDLER.end_product(id)


def Summary(**params):
    PRODUCT_HANDLER.summary()
