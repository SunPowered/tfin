from tests.engine.conftest import BaseTestEvent

from tfin.engine import EngineState

def test_engine_init(engine):
    """Test the engine is initialized correctly before setting up the environment"""
    assert engine.is_state(EngineState.WAITING), "Engine state should init to WAITING"
    assert "initialized" in engine.message.lower(), "Engine init message not set"


def test_engine_str(engine):
    """Test the custom str representation of the engine"""
    for i in range(3):
        engine.schedule(BaseTestEvent(timestep=i, name=f"Event {i}"))
    assert "3 events" in str(engine), str(engine)
