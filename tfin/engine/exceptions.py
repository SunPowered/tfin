from .event import Event

class EngineError(Exception):  # pragma: no cover
    """The simulation encountered an error"""

    def __init__(self, now: int, msg: str):

        self.now = now
        self.message = msg
        super().__init__(str(self))

    def __str__(self):
        return f"{self.now}: {self.message}"

class UnhandledEngineError(EngineError):
    """An exception was caught by the engine that has not been handled, this error encapsulates that event"""

    def __init__(self, now: int, exc: Exception):
        self.exc = exc
        super().__init__(now, f"The Engine encoutered an unhandled exception.  {exc.__class__.__name__}: {exc}")


class EventError(Exception):
    """Base error raised by Events"""

    def __init__(self, event: Event, msg: str):
        self.event = event
        super().__init__(msg)


class StopEngineError(EventError):
    """Raised by Events to indicate that the simulation should be aborted"""
