# Getting Started with tFin

This page will help you to get up and running with the `tfin` package.

## Event simulator

First, you should understand the event simulator engine that is at the heart

```python

from tfin.engine import Engine, Event, StopEvent, EngineState

engine = Engine()

class MyEvent(Event):
    name = "My Event" 

    def __call__(self):
        print(f"Called {self.name} at tick: {self.timestep}")
        return iter([])
engine.schedule(MyEvent(), timestep=3)
engine.run()

assert engine.now == 3
assert engine.state == EngineState
```

This snippet of code created a custom Event that simply prints to the console. 
The engine scheduled the event at a given timestep and the event was processed 
and called at the appropriate timestep.  


