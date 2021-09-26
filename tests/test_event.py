"""Test the Event class"""

from tfin.event import Event


class CoreEvent(Event):
    def call(self):
        print(f"Calling {self.name} at t: {self.timestamp}")
        yield None


def event_factory(
    timestamp: int, name: str = "Test Event", data: dict = {}
) -> CoreEvent:
    return CoreEvent(timestamp, name, data)


def test_event_priority():
    """Test the priority ordering of events"""
    event1, event2, event7 = [event_factory(ts) for ts in [1, 2, 7]]

    event_list = [event2, event7, event1]
    assert sorted(event_list)[0] == event1, list(sorted(event_list))
