from abc import abstractmethod
from typing import runtime_checkable, Iterator, Protocol

@runtime_checkable
class EventLike(Protocol):
    """An Event like interface to use in typing"""

    timestep: int
    name: str

    @abstractmethod
    def call(self, *args):
        """Executes the event callback"""


class Event:
    """The core Event object"""

    def __init__(self, timestep: int, name: str, data: dict = {}):
        self.timestep = timestep
        self.name = name
        self.data = data

    def call(self, ctx: dict = {}) -> Iterator["Event" | None]:
        """The event callback function.

        This is the business end of the event.  It's job is to decide from the context which events to fire and when.

        The function yields events until exhausted.  The engine will consume all yielded events and execute them in
        the order they are yielded.

        The engine will pass a yet ill-defined simulation context dictionary that should contain all relevant context
        objects an event would need
        """
        yield None
