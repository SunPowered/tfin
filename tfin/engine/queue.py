import heapq
from dataclasses import dataclass, field

from .event import Event

@dataclass(order=True)
class QueueItem:
    """A queued event item.  Queues are ordered by the timestep value"""
    timestep: int
    event: Event = field(compare=False)

class EngineQueue:
    """The Event queue for the Engine
    
    It is a simple wrapper around the `heapq` package"""

    def __init__(self):

        self._queue: list[QueueItem] = []

    def push(self, event: Event, timestep: int):

        heapq.heappush(self._queue, QueueItem(timestep=timestep, event=event))

    def pop(self) -> QueueItem:

        return heapq.heappop(self._queue)
    
    def __len__(self) -> int:
        return len(self._queue)