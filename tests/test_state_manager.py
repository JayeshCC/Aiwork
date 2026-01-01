from aiwork.memory.state_manager import StateManager


def test_state_manager_local_store():
    sm = StateManager(use_redis=False)
    sm.save_state("flow1", {"status": "ok"})
    assert sm.get_state("flow1") == {"status": "ok"}


def test_state_manager_redis_stub():
    sm = StateManager(use_redis=True)
    sm.save_state("flow2", {"status": "ok"})
    assert sm.get_state("flow2") == {}
