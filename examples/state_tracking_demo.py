"""
State Tracking Demo
===================

Demonstrates workflow state management:
- Workflow and task status tracking
- State queries during execution
- Recovery from failures

Run with:
    python examples/state_tracking_demo.py
"""

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator
from aiwork.memory.state_manager import StateManager
import time

# Create state manager
state_manager = StateManager()

# Create orchestrator with state tracking
orchestrator = Orchestrator(state_manager=state_manager)

# Define tasks
def slow_task(ctx):
    """Simulate slow task."""
    print("    [Task] Processing... (simulating delay)")
    time.sleep(1)
    return {"result": "processed"}

def dependent_task(ctx):
    """Task that depends on previous task output."""
    prev_result = ctx["outputs"]["process"]
    return {"status": "done", "previous": prev_result}

task1 = Task("process", handler=slow_task)
task2 = Task("finalize", handler=dependent_task)

# Create flow
flow = Flow("demo_flow")
flow.add_task(task1)
flow.add_task(task2, depends_on=["process"])

# Execute workflow
print("=== Starting Workflow ===\n")
result = orchestrator.execute(flow, {})

workflow_id = result["workflow_id"]
print(f"\nWorkflow ID: {workflow_id}")

# Query final state
print("\n=== Final State ===")
final_state = state_manager.get_workflow_state(workflow_id)
print(f"Status: {final_state['status']}")
print(f"Workflow Name: {final_state['name']}")
print(f"Tasks completed: {len([t for t in final_state['tasks'].values() if t['status'] == 'COMPLETED'])}/{len(final_state['tasks'])}")

# Query specific task
print("\n=== Task Details ===")
task_status = state_manager.get_task_status(workflow_id, "process")
print(f"Task 'process' status: {task_status}")
task_output = final_state['tasks']['process']['output']
print(f"Task 'process' output: {task_output}")

task_status = state_manager.get_task_status(workflow_id, "finalize")
print(f"Task 'finalize' status: {task_status}")
task_output = final_state['tasks']['finalize']['output']
print(f"Task 'finalize' output: {task_output}")

# Demonstrate failure tracking
print("\n\n=== Testing Failure Tracking ===\n")

def failing_task(ctx):
    raise ValueError("Simulated failure for demonstration")

fail_flow = Flow("failing_demo")
fail_flow.add_task(Task("failing_task", handler=failing_task))

fail_result = orchestrator.execute(fail_flow, {})
fail_workflow_id = fail_result["workflow_id"]

fail_state = state_manager.get_workflow_state(fail_workflow_id)
print(f"\nFailed Workflow Status: {fail_state['status']}")
print(f"Error: {fail_state['error']}")
print(f"Failed Task Status: {fail_state['tasks']['failing_task']['status']}")

print("\n=== Demo Complete ===")
print("\nKey takeaways:")
print("- Each workflow execution gets a unique ID")
print("- Workflow and task states are tracked automatically")
print("- State can be queried at any time via StateManager")
print("- Failures are captured with error messages")
print("- All state includes timestamps for audit trails")
