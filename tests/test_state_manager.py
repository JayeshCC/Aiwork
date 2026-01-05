from aiwork.memory.state_manager import StateManager
from aiwork.orchestrator import Orchestrator
from aiwork.core.task import Task
from aiwork.core.flow import Flow


def test_state_manager_local_store():
    sm = StateManager(use_redis=False)
    sm.save_state("flow1", {"status": "ok"})
    assert sm.get_state("flow1") == {"status": "ok"}


def test_state_manager_redis_stub():
    sm = StateManager(use_redis=True)
    sm.save_state("flow2", {"status": "ok"})
    assert sm.get_state("flow2") == {}


def test_workflow_state_tracking():
    """Test StateManager tracks workflow execution."""
    state_manager = StateManager()
    orchestrator = Orchestrator(state_manager=state_manager)
    
    task = Task("test", handler=lambda ctx: {"result": 42})
    flow = Flow("test_flow")
    flow.add_task(task)
    
    result = orchestrator.execute(flow, {})
    workflow_id = result["workflow_id"]
    
    # Check workflow tracked
    state = state_manager.get_workflow_state(workflow_id)
    assert state["status"] == "COMPLETED"
    assert state["name"] == "test_flow"
    assert "created_at" in state
    assert "updated_at" in state
    
    # Check task tracked
    task_status = state_manager.get_task_status(workflow_id, "test")
    assert task_status == "COMPLETED"
    
    # Check task output stored
    assert state["tasks"]["test"]["output"] == {"result": 42}


def test_task_status_tracking():
    """Test task status transitions are tracked."""
    state_manager = StateManager()
    orchestrator = Orchestrator(state_manager=state_manager)
    
    # Create tasks with dependencies
    task1 = Task("first", handler=lambda ctx: "data1")
    task2 = Task("second", handler=lambda ctx: ctx["outputs"]["first"] + "_data2")
    
    flow = Flow("multi_task_flow")
    flow.add_task(task1)
    flow.add_task(task2, depends_on=["first"])
    
    result = orchestrator.execute(flow, {})
    workflow_id = result["workflow_id"]
    
    # Verify both tasks completed
    state = state_manager.get_workflow_state(workflow_id)
    assert state["tasks"]["first"]["status"] == "COMPLETED"
    assert state["tasks"]["second"]["status"] == "COMPLETED"
    assert state["tasks"]["first"]["output"] == "data1"
    assert state["tasks"]["second"]["output"] == "data1_data2"


def test_workflow_failure_tracking():
    """Test workflow failures are tracked properly."""
    state_manager = StateManager()
    orchestrator = Orchestrator(state_manager=state_manager)
    
    def failing_handler(ctx):
        raise ValueError("Intentional failure")
    
    task = Task("failing_task", handler=failing_handler)
    flow = Flow("failing_flow")
    flow.add_task(task)
    
    result = orchestrator.execute(flow, {})
    workflow_id = result["workflow_id"]
    
    # Verify workflow failure tracked
    state = state_manager.get_workflow_state(workflow_id)
    assert state["status"] == "FAILED"
    assert state["error"] == "Intentional failure"
    
    # Verify task failure tracked
    assert state["tasks"]["failing_task"]["status"] == "FAILED"
    assert state["tasks"]["failing_task"]["error"] == "Intentional failure"


def test_get_workflow_state_not_found():
    """Test get_workflow_state raises error for non-existent workflow."""
    state_manager = StateManager()
    
    try:
        state_manager.get_workflow_state("non-existent-id")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not found" in str(e)
