  
class Event:
    """
    The base Event class to be subclassed by user events
    """
    def __init__(self, timestep: int | None = None, name: str | None = None):

        self.timestep = timestep
        self.name = name

    def __call__(self, **kwargs):

        return iter([])
