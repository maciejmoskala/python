import os
import yaml
from urllib.request import urlopen
from stock_synchronizer.globals import ROOT
from stock_synchronizer.globals import DEFAULT_INPUT_FILE
from stock_synchronizer.globals import DEFAULT_OUTPUT_FILE

_SETTINGS = None
_PLACEHOLDER = object()
_ENV_CONF = 'CONF_URL'
_ENV_INPUT_FILE = 'INPUT_FILE'
_ENV_OUTPUT_FILE = 'OUTPUT_FILE'


def _read_default_config():
    with open(os.path.join(ROOT, 'default.yaml'), 'rb') as fo:
        data = fo.read()
    return yaml.load(data.decode('utf-8'))


def load():
    global _SETTINGS
    if _SETTINGS is not None:
        raise RuntimeError('Settings already initialized!')

    config = _read_default_config()
    config['config'] = 'default'

    url = os.environ.get(_ENV_CONF)
    if url is not None:
        request = urlopen(url)
        data = request.read()
        try:
            data = yaml.load(data.decode('utf-8'))
        except Exception:
            raise RuntimeError('Resource under [{}] is not a valid yaml!'.format(url))
        config['config'] = url
        config.update(data)

    input_file = os.environ.get(_ENV_INPUT_FILE, DEFAULT_INPUT_FILE)
    config['input_file'] = input_file

    output_file = os.environ.get(_ENV_OUTPUT_FILE, DEFAULT_OUTPUT_FILE)
    config['output_file'] = output_file

    _SETTINGS = config


def get_all():
    global _SETTINGS
    if _SETTINGS is None:
        raise RuntimeError('Setting not initialized!')
    return _SETTINGS


def get(key, default=_PLACEHOLDER):
    settings = get_all()
    try:
        return settings[key]
    except KeyError:
        if default is not _PLACEHOLDER:
            return default
        raise
