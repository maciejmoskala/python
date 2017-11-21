import ujson
import pytest
from stock_synchronizer.core.input_event import JsonInputEvent
from stock_synchronizer.core.event_processor import process_event
from stock_synchronizer.core.rpc import initialize as initialize_rpc


class TestJsonInputEvent:

    @pytest.fixture(scope="module")
    def init_rpc(self):
        initialize_rpc()

    def test_process_event(self, init_rpc):
        dct = {
            'type': 'ProductCreated',
            'timestamp': 123,
            'id': 1,
            'parent_id': None,
            'stock': 10,
        }
        input_event = JsonInputEvent.from_dict(dct)
        process_event(input_event)

    def test_process_event_incorrect_method(self, init_rpc):
        dct = {
            'type': 'UnknownMethod',
            'timestamp': 123,
            'id': 1,
            'parent_id': None,
            'stock': 10,
        }
        input_event = JsonInputEvent.from_dict(dct)
        with pytest.raises(Exception):
            process_event(input_event)

    def test_process_event_incorrect_timestamp(self, init_rpc):
        dct = {
            'type': 'ProductCreated',
            'timestamp': -1,
            'id': 1,
            'parent_id': None,
            'stock': 10,
        }
        input_event = JsonInputEvent.from_dict(dct)
        with pytest.raises(Exception):
            process_event(input_event)
