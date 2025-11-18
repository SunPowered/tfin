import pytest
from tfin.engine import Engine, Event

@pytest.fixture
def engine():
    return Engine()


class EmptyEvent(Event):
    """An event to use in testing"""

    def __init__(self, timestep: int, name:str):
        self.timestep = timestep
        self.name = name

    def call(self):
        return iter([])
     
def event_factory(event_cls=EmptyEvent, timestep=0, name="Test Event", event_kwargs={}):
    return event_cls(timestep=timestep, name=name, **event_kwargs)
