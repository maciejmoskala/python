import pytest
from stock_synchronizer import settings


# AUTOUSE FIXTURES
@pytest.fixture(scope='session', autouse=True)
def load_settings():
    settings.load()
