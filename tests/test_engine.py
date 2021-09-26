"""Test the Event engine"""
import pytest
from tfin.engine import Engine, EngineState
from tfin.event import Event, EventError, StopEngineError


@pytest.fixture
def engine():
    return Engine()


class EmptyEvent(Event):
    """An event to use in testing"""


def event_factory(event_cls=EmptyEvent, timestamp=0, name="Test Event", data={}):
    return event_cls(timestamp=timestamp, name=name, data=data)


def test_engine_scheduling(engine):
    """Tests that the engine schedules events sorted by timestamp"""
    assert len(engine.queue) == 0, "Queue not empty"
    event = event_factory(timestamp=3)
    engine.schedule(event)
    assert len(engine.queue) == 1, "Queue still empty"
    assert engine.queue[0] == event

    event2 = event_factory(timestamp=1)
    engine.schedule(event2)

    assert engine.queue[0] == event2, "Queue priority not being enforced"


def test_engine_schedule_bad_input(engine):
    """Ensure only subclasses of Event is added to the queue"""
    engine.schedule({"name": "event"})
    engine.schedule("MyEvent")
    engine.schedule(42)
    assert len(engine.queue) == 0, "Bad data structure added to queue"


def test_engine_init(engine):
    """Test the engine is initialized correctly before setting up the environment"""
    assert engine.is_state(EngineState.WAITING), "Engine state should init to WAITING"
    assert "initialized" in engine.message.lower(), "Engine init message not set"


def test_engine_str(engine):
    """Test the custom str representation of the engine"""
    for i in range(3):
        engine.schedule(event_factory(timestamp=i))

    assert "3 events" in str(engine), str(engine)


def test_engine_status_finished(engine):
    """Tests when the engine is finished exhausting the event queue"""

    engine.schedule(event_factory())

    engine.run()

    assert engine.is_state(
        EngineState.FINISHED
    ), f"Engine state should be FINISHED, got {engine.state}"


def test_engine_status_stopped(engine):
    """Tests when the engine stops itself at a fixed time"""
    engine.schedule(event_factory(timestamp=1))
    engine.schedule(event_factory(timestamp=5))

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

    class StopEvent(Event):
        def call(self):
            raise StopEngineError(self, "I've been a bad event")

    engine.schedule(event_factory(StopEvent))
    engine.run()

    assert (
        engine.state == EngineState.STOPPED
    ), "StopSimulationError did not trigger an engine STOP"


def test_engine_abort(engine):
    """Tests status when an event purposefully errors out"""

    class ErroredEvent(Event):
        def call(self):
            raise EventError(self, "This is a general error")

    engine.schedule(event_factory(ErroredEvent))
    engine.run()

    assert (
        engine.state == EngineState.ABORTED
    ), "Errored event did not trigger an engine ABORT"


def test_engine_error(engine):
    """Tests when an event errors out unexpectedly"""

    class EvilEvent(Event):
        def call(self, *args):
            raise ValueError("This is a poorly written event")

    engine.schedule(event_factory(EvilEvent))
    with pytest.raises(ValueError):
        engine.run()


def test_engine_consuming_events(engine):
    """Test the engine consuming an event that yields several new events"""

    class SimpleEvent(Event):
        """Event that yields several empty events"""

        def call(self):
            for i in range(3):
                yield EmptyEvent(self.timestamp + 2 * i, f"Yielded Event {i}")

    engine.schedule(SimpleEvent(2, "Top Event"))
    engine.run()

    assert engine.state == EngineState.FINISHED, "Engine is in wrong state"
    assert engine.now == 6, f"Simulation should be at timestep 6, not {engine.now}"
