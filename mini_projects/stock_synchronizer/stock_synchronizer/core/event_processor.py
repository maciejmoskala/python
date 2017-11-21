from stock_synchronizer.core.rpc import REGISTRY
from stock_synchronizer.core.exceptions import EventNotFound
from stock_synchronizer.core.exceptions import MethodNotFound
from stock_synchronizer.core.exceptions import OutdatedEvent

TIMESTAMP = 0


def process_event(event):
    method = REGISTRY.get(event.method)
    if method is None:
        raise MethodNotFound('Unknown method %s.' % event.method)

    global TIMESTAMP
    if event.timestamp:
        if event.timestamp <= TIMESTAMP:
            raise OutdatedEvent('Outdated event.' % event.timestamp)
        TIMESTAMP = event.timestamp

    method(**event.params)
