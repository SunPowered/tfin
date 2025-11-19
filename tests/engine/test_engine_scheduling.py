import pytest

from tests.engine.conftest import BaseTestEvent

from tfin.engine import EngineState, StopEngineError, EventError, UnhandledEngineError


def test_engine_status_finished(engine):
    """Tests when the engine is finished exhausting the event queue"""

    engine.schedule(BaseTestEvent(timestep=engine.now))

    engine.run()

    assert engine.is_state(
        EngineState.FINISHED
    ), f"Engine state should be FINISHED, got {engine.state}"


def test_engine_status_stopped(engine):
    """Tests when the engine stops itself at a fixed time"""
    engine.schedule(BaseTestEvent(timestep=1), timestep=1)
    engine.schedule(BaseTestEvent(timestep=5), timestep=5)

    stop_at = 3
    engine.run(stop_at=stop_at)

    assert engine.is_state(
        EngineState.STOPPED
    ), f"Engine state should be STOPPED, got {engine.state}"

    assert (
        engine.now == stop_at
    ), f"Simulation time should be stopped at {stop_at}, not {engine.now}"


def test_engine_stopped_by_event(engine):
    """Tests when an event forces the engine to stop"""

    class TestStopEvent(BaseTestEvent):
        def __init__(self, timestep:int = 0, name: str = "Test Stop Event"):
            self.timestep = timestep
            self.name = name

        def call(self):
            raise StopEngineError(self, "I've been a bad event")

    engine.schedule(TestStopEvent(timestep=engine.now))
    engine.run()

    assert (
        engine.state == EngineState.STOPPED
    ), "StopEngineError did not trigger an engine STOP"


def test_engine_abort(engine):
    """Tests status when an event purposefully errors out"""

    class ErroredEvent(BaseTestEvent):
        def __init__(self, timestep:int=0, name="Error Event"):
            self.timestep = timestep
            self.name = name

        def call(self):
            raise EventError(self, "This is a general error produced by the engine")

    engine.schedule(ErroredEvent(timestep=engine.now))
    engine.run()

    assert (
        engine.state == EngineState.ABORTED
    ), "Errored event did not trigger an engine ABORT"


def test_engine_error(engine):
    """Tests when an event errors out unexpectedly"""

    class TestEvilEvent(BaseTestEvent):
        def __init__(self, timestep=0, name="Evil Event"):
            self.timestep = timestep
            self.name = name

        def call(self):
            raise ValueError("This is an unhandled exception in the event")

    engine.schedule(TestEvilEvent())
    with pytest.raises(UnhandledEngineError):
        engine.run()


def test_engine_consuming_events(engine):
    """Test the engine consuming an event that yields several new events"""

    class SimpleEvent(BaseTestEvent):
        """Event that yields several empty events"""

        def __init__(self, timestep:int, name="Top Event"):
            self.timestep = timestep
            self.name = name
            
        def call(self):
            for i in range(3):
                yield BaseTestEvent(self.timestep + 2 * i, f"Yielded Event {i}")

    engine.schedule(SimpleEvent(2, "Top Event"), timestep=2)
    engine.run()

    assert engine.state == EngineState.FINISHED, "Engine is in wrong state"
    assert engine.now == 6, f"Simulation should be at timestep 6, not {engine.now}"

def test_scheduling_event_with_timestampt(engine):
    """Schedule events with and without timestamp"""
    engine.schedule(BaseTestEvent(timestep=3))

    engine.schedule(BaseTestEvent(), timestep=4)

    assert len(engine.queue) == 2

    queue_item = engine.queue.pop()
    assert queue_item.event.timestep == queue_item.timestep
    assert queue_item.timestep == 3

    queue_item = engine.queue.pop()
    assert queue_item.event.timestep == queue_item.timestep
    assert queue_item.timestep == 4

    engine.schedule(BaseTestEvent())
    
    queue_item = engine.queue.pop()
    assert queue_item.event.timestep == queue_item.timestep
    assert queue_item.timestep == engine.now

