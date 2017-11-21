import os
import pytest
from unittest import mock
from stock_synchronizer import settings


class TestLoad:
    @pytest.fixture(scope='session')
    def root(self):
        return os.path.dirname(os.path.realpath(__file__))

    def test_double_load(self):
        with pytest.raises(RuntimeError):
            settings.load()

    @mock.patch('stock_synchronizer.settings._SETTINGS', new=None)
    def test_invalid_load(self, root):
        url = 'file:{}/test_incorrect_config.xyz'.format(root)
        with mock.patch('os.environ', new={'CONF_URL': url}):
            with pytest.raises(RuntimeError):
                settings.load()

    @mock.patch('stock_synchronizer.settings._SETTINGS', new=None)
    def test_valid_load(self, root):
        url = 'file:{}/test_config.yaml'.format(root)
        with mock.patch('os.environ', new={'CONF_URL': url}):
            settings.load()
        assert settings.get('key') == 0
        assert settings.get('foo') == 'bar'


class TestGet:
    def test_get(self):
        assert isinstance(settings.get('logger'), dict)

    def test_get_default(self):
        value = settings.get('logger', 1)
        assert isinstance(value, dict)

    def test_get_no_key(self):
        with pytest.raises(KeyError):
            settings.get('xyz')

    def test_get_no_key_default(self):
        value = settings.get('xyz', 1)
        assert value == 1


class TestGetAll:
    def test_get_all(self):
        all_settings = settings.get_all()
        assert isinstance(all_settings, dict)
        assert set(all_settings.keys()) == {
            'config', 'output_file', 'input_file', 'logger'
        }
        assert all_settings['config'] == 'default'

    @mock.patch('stock_synchronizer.settings._SETTINGS', new=None)
    def test_get_all_no_settings(self):
        with pytest.raises(RuntimeError):
            settings.get_all()
