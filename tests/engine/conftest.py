import pytest
from tfin.engine import Engine, Event

@pytest.fixture
def engine():
    return Engine()


class EmptyEvent(Event):
    """An event to use in testing"""


def event_factory(event_cls=EmptyEvent, timestep=0, name="Test Event", data={}):
    return event_cls(timestep=timestep, name=name, data=data)
