from enum import Enum, auto

class EngineState(Enum):
    """Enumeration of allowed engine states"""

    WAITING = auto()  # Initial state of a fresh simulation
    STOPPED = auto()  # Simulation was stopped early for a reason
    RUNNING = auto()  # Simulation is in a normal running state
    PAUSED = auto()  # Simulation was paused by the user
    ABORTED = auto()  # Simulation was aborted due to error
    FINISHED = auto()  # Simulation completed normally
