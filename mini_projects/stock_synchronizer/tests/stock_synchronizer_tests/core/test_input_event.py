import json
import pytest
from stock_synchronizer.core.input_event import JsonInputEvent


class TestJsonInputEvent:

    @pytest.fixture
    def input_event_dct(self):
        dct = {
            'type': 'ProductCreated',
            'timestamp': 123,
            'id': 1,
            'parent_id': None,
            'stock': 10,
        }
        return dct

    @pytest.fixture
    def input_event_json(self, input_event_dct):
        return json.dumps(input_event_dct)

    def test_from_dict_correct_event(self, input_event_dct):
        inst = JsonInputEvent.from_dict(input_event_dct)
        assert inst.method == input_event_dct['type']
        assert inst.timestamp == input_event_dct['timestamp']
        assert isinstance(inst.params, dict)

    def test_from_dict_incorrect_event_structure(self, input_event_dct):
        del input_event_dct['timestamp']
        with pytest.raises(Exception):
            JsonInputEvent.from_dict(input_event_dct)

    def test_from_json_correct_event(self, input_event_dct, input_event_json):
        inst = JsonInputEvent.from_json(input_event_json)
        assert inst.method == input_event_dct['type']
        assert inst.timestamp == input_event_dct['timestamp']
        assert isinstance(inst.params, dict)

    def test_from_json_incorrect_event(self, input_event_json):
        incorrect_json_message = input_event_json.replace('\"', '\'')
        with pytest.raises(Exception):
            JsonInputEvent.from_json(incorrect_json_message)
