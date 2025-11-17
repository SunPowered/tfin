from .event import Event

class EngineError(Exception):  # pragma: no cover
    """The simulation encountered an error"""

    def __init__(self, now: int, msg: str):

        self.now = now
        self.message = msg
        super().__init__(str(self))

    def __str__(self):
        return f"{self.now}: {self.message}"


class EventError(Exception):
    """Base error raised by Events"""

    def __init__(self, event: Event, msg: str):
        self.event = event
        super().__init__(msg)


class StopEngineError(EventError):
    """Raised by Events to indicate that the simulation should be aborted"""
