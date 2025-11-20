from dataclasses import dataclass

from .enums import EngineState
from .event import Event
from .queue import EngineQueue, QueueItem
from .exceptions import EventError, StopEngineError, UnhandledEngineError

@dataclass
class EngineStatus:
    """Data structure to hold the current simulation status"""

    state: EngineState
    message: str

class Engine:
    """The core simulation engine.

    The engine is responsible for managing the event queue and running the entire simulation
    """

    def __init__(self, name: str | None = None):
        self.name = name
        self.now = 0
        self.queue = EngineQueue()
        self._status = EngineStatus(
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

    def schedule(self, event: Event, timestep: int | None = None) -> None:
        """Schedule an event to the queue"""

        if timestep is None:
            if event.timestep is None:
                timestep = self.now
                event.timestep = timestep
            else:
                timestep = event.timestep
        elif event.timestep is None:
            event.timestep = timestep
        
        if timestep < self.now:
            raise ValueError(f"Cannot schedule event {event} in the past: {timestep} < {self.now}")

        self.queue.push(event, timestep)
        
    def stop(self, msg: str) -> None:
        """Stops the engine with a message"""
        self.set_status(EngineState.STOPPED, msg)

    def abort(self, msg: str) -> None:
        """Aborts the engine with a message"""
        self.set_status(EngineState.ABORTED, msg)

    def finish(self, msg: str) -> None:
        """Finish the program"""
        self.set_status(EngineState.FINISHED, msg)

    def run(self, stop_at: int | None = None) -> None:
        """Runs the simulation.

        This involves continually retrieving events from the queue until
        it either is exhausted or the timestep reaches a given `stop` time.
        """

        self.set_status(
            EngineState.RUNNING, f"Stopping at {stop_at if stop_at else 'Never'}"
        )

        while True:
            try:
                queue_item = self.queue.pop()
            except IndexError:
                self.finish(f"Simulation finished at {self.now}")
                return
            
            timestep = queue_item.timestep
            event = queue_item.event
            
            if stop_at is not None and timestep > stop_at:
                self.now = stop_at
                self.stop(f"Simulation max time {stop_at} exceeded")
                return
            else:
                self.now = timestep

            if not self.consume_event(event):
                return

    def consume_event(self, event: Event):
        """Processes an event, checks for errors and schedules any events that are yielded"""
        try:
            for evt in event():
                if evt:
                    self.schedule(evt)

        except StopEngineError as e:
            self.stop(
                f"Simulation was stopped by event {event.name} at t {self.now}: {e}"
            )
            return False
        except EventError as e:
            self.abort(
                f"Simulation was aborted by event {event.name} at t{self.now}: {e}"
            )
            return False
        except Exception as e:
            raise UnhandledEngineError(self.now, e)
        else:
            return True
        return False