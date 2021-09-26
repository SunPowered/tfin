"""The core event-based simulation engine"""
import heapq
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, NamedTuple

from .event import EventError, EventLike, StopEngineError

__all__ = ["Engine", "EngineError", "EngineState", "EngineStatus"]


class EngineError(Exception):  # pragma: no cover
    """The simulation encountered an error"""

    def __init__(self, now: int, msg: str):

        self.now = now
        self.message = msg
        super().__init__(str(self))

    def __str__(self):
        return f"{self.now}: {self.message}"


class EngineState(Enum):
    """Enumeration of allowed engine states"""

    WAITING = auto()  # Initial state of a fresh simulation
    STOPPED = auto()  # Simulation was stopped early for a reason
    RUNNING = auto()  # Simulation is in a normal running state
    PAUSED = auto()  # Simulation was paused by the user
    ABORTED = auto()  # Simulation was aborted due to error
    FINISHED = auto()  # Simulation completed normally


class EngineStatus(NamedTuple):
    """Data structure to hold the current simulation status"""

    state: EngineState
    message: str


@dataclass
class Engine:
    """The core simulation engine.

    The engine is responsible for managing the event queue and running the entire simulation
    """

    name: str = "Unnamed"  # The name of this engine

    def __post_init__(self):
        self.now = 0
        self.queue: List[EventLike] = []
        self._status: EngineStatus = EngineStatus(
            state=EngineState.WAITING,
            message="Initialized",
        )

    def __str__(self):
        return f"Engine({self.name}) - {len(self.queue)} events - Status: '{self.state.name}'"

    @property
    def status(self):
        """The status of the engine holds an `EngineStatus` object comprising of the current engine state and a message"""
        return self._status

    def set_status(self, state: EngineState, message: str):
        """Setter method for the engine status"""
        self._status = EngineStatus(state=state, message=message)

    @property
    def state(self) -> EngineState:
        """The engine state is an `Enginestate` enumerated object of allowed states"""
        return self.status.state

    @property
    def message(self) -> str:
        """The latest engine status message"""
        return self.status.message

    def is_state(self, state: EngineState) -> bool:
        """Returns whether the current engine state evaluates to the provided one"""
        return self.state == state

    def schedule(self, event: EventLike) -> None:
        """Schedule an event to the queue"""

        if isinstance(event, EventLike):
            heapq.heappush(self.queue, event)

    def stop(self, msg: str) -> None:
        """Stops the engine with a message"""
        self.set_status(EngineState.STOPPED, msg)

    def abort(self, msg: str) -> None:
        """Aborts the engine with a message"""
        self.set_status(EngineState.ABORTED, msg)

    def finish(self, msg: str) -> None:
        """Finish the program"""
        self.set_status(EngineState.FINISHED, msg)

    def run(self, stop_at: int = None) -> None:
        """Runs the simulation.

        This involves continually retrieving events from the queue until
        it either is exhausted or the timestep reaches a given `stop` time.
        """

        self.set_status(
            EngineState.RUNNING, f"Stopping at {stop_at if stop_at else 'Never'}"
        )

        while True:
            if not self.queue:
                self.finish(f"Simulation finished at {self.now}")
                return

            event = heapq.heappop(self.queue)

            if stop_at is not None and event.timestamp > stop_at:
                self.now = stop_at
                self.stop(f"Simulation max time {stop_at} exceeded")
                return
            else:
                self.now = event.timestamp

            if not self.consume_event(event):
                return

    def consume_event(self, event: EventLike):
        """Processes an event, checks for errors and schedules any events that are yielded"""
        try:
            for evt in event():
                if evt:
                    self.schedule(evt)

        except StopEngineError as e:
            self.stop(f"Simulation was stopped by event {event} at t {self.now}: {e}")
        except EventError as e:
            self.abort(f"Simulation was aborted by event {event} at t{self.now}: {e}")
        else:
            return True
