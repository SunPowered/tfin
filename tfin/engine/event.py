
from typing import Iterator, Protocol

# @runtime_checkable
class Event(Protocol):
    """The core Event object"""

    timestep: int       # The timestep to process the event
    name: str           # The name of the event

    def call(self, **kwargs) -> Iterator[Event]:
        """The event callback function.

        This is the business end of the event.  It's job is to decide from the context which events to fire and when.

        The function yields events until exhausted.  The engine will consume all yielded events and execute them in
        the order they are yielded.

        The engine will pass a yet ill-defined simulation context dictionary that should contain all relevant context
        objects an event would need
        """
        ...

class BaseEvent:
    """
    The base Event class to be subclassed by user events
    
    TODO: Allow timestep = None and have the Engine assign it to the next available timestep when scheduled
    """
    def __init__(self, timestep: int, name: str | None = None):

        self.timestep = timestep
        self.name = name or "Unnamed Event"

    def call(self):

        return iter([])

