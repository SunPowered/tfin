import pytest
from tfin.engine import Engine, BaseEvent

@pytest.fixture
def engine():
    return Engine()


class BaseTestEvent(BaseEvent):
    """An event to use in testing"""
    pass     

