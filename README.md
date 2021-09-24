# TFin

A pet project to develop an event based financial simulator.

Author: TvB - 2021

## Goals

The primary objective of this project is to be able to model real world business scenarios.

This is an attempt to integrate fuzzy/probabilistic business logic, financial accounting, reporting and Monte Carlo simulations to evaluate
 simulation targets and input sensitivities. 

## Architecture 

The software is backed by an Event Engine that manages its own status and a priority event queue as well as executes 
event callbacks.  

Events are low level abstract objects that are intended to be subclassed for specific implementations. 
Events  store data of when to execute and other data that is needed when called.   Once initiated, events can be
called like a funtion by the engine.  Using custom exception handling, events can direct special cases to the Engine, 
such as forcing it to Abort, or Stop.  

The intent is to have Events able to generate and schedule other events in the engine (ie repeating every week) or to fire special events 
if a certain condition is met.  This way, the simulation can be autogenerating and behaviour is encoded in the actors or events.  

Events will yield other events when called.  This allows for effective decoupling of events / engine when calling.  

## Development

Currently in a state of heavy development.  No API is safe. 

### Setup

The main project language is Python 3.8+.  Environment management is done using `poetry`, 
this must be installed locally.  

`python -m pip install poetry`

To set up the project environment
`poetry install`

### Testing

To run the test suite:

`poetry run pytest [args]`

I like to run with coverage before committing changes; there is a `.coveragerc` file configured:

`poetry run pytest --cov`

It is expected that any active non-debug feature is covered by the test suite, and anything else is properly ignored.  

100% coverage can be done!  I believe in us.

## History

* 0.1.0 - Sep 2021 - Project structure, basic event and event engine