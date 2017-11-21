import ujson
import pytest
from stock_synchronizer.core.output_event import JsonOutputEvent


class TestJsonOutputEvent:

    @pytest.fixture
    def output_event_dct(self):
        dct = {
            'method': 'Method',
            'param': 123,
        }
        return dct

    @pytest.fixture
    def output_event(self, output_event_dct):
        params = dict(output_event_dct)
        output_event = JsonOutputEvent(
            method=params['method'],
            param=params['param']
        )
        return output_event

    def test_to_dict(self, output_event_dct, output_event):
        dct_inst = output_event.to_dict()
        assert dct_inst['method'] == output_event_dct['method']
        assert dct_inst['param'] == output_event_dct['param']

    def test_to_json(self, output_event_dct, output_event):
        json_inst = output_event.to_json()
        dct_inst = ujson.loads(json_inst)
        assert dct_inst['method'] == output_event_dct['method']
        assert dct_inst['param'] == output_event_dct['param']
