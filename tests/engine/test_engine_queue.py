import pytest

from tests.engine.conftest import BaseTestEvent
from tfin.engine.queue import EngineQueue, QueueItem


def test_engine_queue():
    """Basic sanity check of the engine queue"""
    test_timestep = 2
    queue = EngineQueue()

    assert len(queue) == 0, "Initialized queue not empty"

    queue.push(BaseTestEvent(timestep=test_timestep), test_timestep)

    assert len(queue) == 1, "Queue should have length 1 after pushed event"

    queue_item = queue.pop()

    assert queue_item is not None

    assert isinstance(queue_item, QueueItem)
    assert queue_item.timestep == test_timestep, "Bad timestep in queued item"
    assert isinstance(queue_item.event, BaseTestEvent)

    assert len(queue) == 0

    with pytest.raises(IndexError):
        queue.pop()

def test_engine_queue_priority():

    queue = EngineQueue()

    queue.push(BaseTestEvent(timestep=4, name="Second"), timestep=4)

    queue.push(BaseTestEvent(timestep=2, name="First"), timestep=2)

    assert len(queue) == 2

    queue_item = queue.pop()

    assert queue_item.timestep == 2, "Wrong event item returned from pop()"