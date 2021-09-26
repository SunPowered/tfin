from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, Optional, Protocol, runtime_checkable

__all__ = ["Event", "EventError", "StopEngineError", "EventLike"]


class EventError(Exception):
    """Base error raised by Events"""

    def __init__(self, event: "Event", msg: str):
        self.event = event
        super().__init__(msg)


class StopEngineError(EventError):
    """Raised by Events to indicate that the simulation should be aborted"""


@runtime_checkable
class EventLike(Protocol):
    """An Event like interface to use in typing"""

    timestamp: int
    name: str

    @abstractmethod
    def __call__(self, *args):
        """Executes the event callback"""


@dataclass(order=True)
class Event:
    """The core Event object"""

    timestamp: int
    name: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)

    def __call__(self, *args, **kwargs):
        """Convenience method to wrap the `call` method."""
        return self.call(*args, **kwargs)

    def call(self, ctx: dict = {}) -> Iterator[Optional["Event"]]:
        """The event callback function.

        This is the business end of the event.  It's job is to decide from the context which events to fire and when.

        The function yields events until exhausted.  The engine will consume all yielded events and execute them in
        the order they are yielded.

        The engine will pass a yet ill-defined simulation context dictionary that should contain all relevant context
        objects an event would need
        """
        yield None
