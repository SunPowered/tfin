import pytest
from tfin.engine import Engine, Event

@pytest.fixture
def engine():
    return Engine()


class BaseTestEvent(Event):
    """An event to use in testing"""
    pass     

