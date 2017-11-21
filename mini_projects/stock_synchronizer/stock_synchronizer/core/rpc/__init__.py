from importlib import import_module

REGISTRY = {}


def register_function(fn_path):
    path, fn_name = fn_path.rsplit('.', 1)
    module = import_module(path)
    fn = getattr(module, fn_name)
    if fn_name in REGISTRY:
        raise RuntimeError('rpc method [{}] already registerd.'.format(fn_name))
    REGISTRY[fn_name] = fn


def initialize():
    register_function('stock_synchronizer.core.rpc.product.ProductCreated')
    register_function('stock_synchronizer.core.rpc.product.ProductUpdated')
    register_function('stock_synchronizer.core.rpc.product.ProductEnded')
    register_function('stock_synchronizer.core.rpc.product.Summary')
