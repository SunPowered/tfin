import abc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator, Optional

if TYPE_CHECKING:
    from .engine import Engine  # pragma: no cover

__all__ = ["Event", "EventError", "StopEngineError"]


class EventError(Exception):
    """Base error raised by Events"""

    def __init__(self, event: "Event", msg: str):
        self.event = event
        super().__init__(msg)


class StopEngineError(EventError):
    """Raised by Events to indicate that the simulation should be aborted"""


@dataclass(order=True)
class Event:
    """The core Event object"""

    timestamp: int
    name: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)

    def __call__(self, *args, **kwargs):
        """Convenience method to wrap the `call` method."""
        return self.call(*args, **kwargs)

    @abc.abstractclassmethod
    def call(self, ctx: dict = {}) -> Iterator[Optional["Event"]]:
        """The event callback function.

        This is the business end of the event.  It's job is to decide from the context which events to fire and when.

        The function yields events until exhausted.  The engine will consume all yielded events and execute them in
        the order they are yielded.

        The engine will pass a yet ill-defined simulation context dictionary that should contain all relevant context
        objects an event would need
        """
