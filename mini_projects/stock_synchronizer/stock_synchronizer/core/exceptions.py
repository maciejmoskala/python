class StockSynchronizerException(Exception):
    pass


class EventNotFound(StockSynchronizerException):
    pass


class MethodNotFound(StockSynchronizerException):
    pass


class OutdatedEvent(StockSynchronizerException):
    pass
