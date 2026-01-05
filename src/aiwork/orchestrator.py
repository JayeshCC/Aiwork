from typing import Dict, Any
from .core.flow import Flow
from .executors.local_executor import LocalExecutor
from .memory.state_manager import StateManager
import uuid

class Orchestrator:
    """
    Executes Flows, managing state and dependencies.
    """
    def __init__(self, executor=None, state_manager=None):
        """
        Initialize the Orchestrator.
        
        Args:
            executor: Executor instance to use for task execution.
                     Defaults to LocalExecutor if not provided.
            state_manager: StateManager instance for workflow state tracking.
                          Defaults to new StateManager if not provided.
        """
        self.memory = {}
        self.executor = executor or LocalExecutor()
        self.state_manager = state_manager or StateManager()

    def execute(self, flow: Flow, initial_context: Dict[str, Any] = None, workflow_id: str = None) -> Dict[str, Any]:
        """
        Executes the given flow with state tracking.
        
        Args:
            flow: Flow to execute
            initial_context: Optional initial context dict
            workflow_id: Optional workflow ID (generated if not provided)
        
        Returns:
            Dict with workflow_id and final outputs
        """
        # Generate or use provided workflow ID for tracking
        if workflow_id is None:
            workflow_id = str(uuid.uuid4())
        
        # Initialize context
        context = initial_context or {}
        context["workflow_id"] = workflow_id
        context["outputs"] = {}
        
        # Track workflow start
        self.state_manager.set_workflow_status(workflow_id, "RUNNING", flow.name)
        
        # Get execution order
        try:
            execution_order = flow.get_topological_sort()
        except ValueError as e:
            print(f"Flow Error: {e}")
            self.state_manager.set_workflow_status(workflow_id, "FAILED", flow.name, error=str(e))
            return context

        print(f"Starting Flow: {flow.name}")
        
        # We use a list that can be dynamically appended to
        execution_queue = list(execution_order)
        processed_tasks = set()
        workflow_failed = False

        i = 0
        while i < len(execution_queue):
            task = execution_queue[i]
            i += 1
            
            if task.name in processed_tasks:
                continue

            # Track task start
            self.state_manager.set_task_status(workflow_id, task.name, "RUNNING")

            print(f"  Executing Task: {task.name}...")
            if hasattr(task, 'agent') and task.agent:
                 print(f"    > Assigned to Agent: {task.agent.role}")

            try:
                # Pass the full context to the task via executor
                result = self.executor.execute(task, context)
                context["outputs"][task.name] = result
                processed_tasks.add(task.name)
                
                # Track task completion
                self.state_manager.set_task_status(workflow_id, task.name, "COMPLETED")
                self.state_manager.update_task_output(workflow_id, task.name, result)
                
                print(f"  Task {task.name} Completed.")

                # --- Hybrid Orchestration Logic ---
                # If the result contains new Tasks or a Flow, inject them dynamically
                if isinstance(result, dict) and "next_tasks" in result:
                    new_tasks = result["next_tasks"]
                    print(f"    [Dynamic] Agent requested {len(new_tasks)} new tasks.")
                    execution_queue.extend(new_tasks)
                
                # If the result is a Flow object (Agent defined a sub-flow)
                if isinstance(result, Flow):
                     print(f"    [Dynamic] Agent returned a sub-flow: {result.name}")
                     # For simplicity, just append tasks (in real DAG, we'd need to resolve deps)
                     execution_queue.extend(result.tasks)

            except Exception as e:
                print(f"  Task {task.name} Failed: {e}")
                # Track task failure
                self.state_manager.set_task_status(workflow_id, task.name, "FAILED", error=str(e))
                self.state_manager.set_workflow_status(workflow_id, "FAILED", flow.name, error=str(e))
                workflow_failed = True
                # In a real system, handle retries or stop flow
                break
        
        print(f"Flow {flow.name} Finished.")
        # Only mark as COMPLETED if workflow didn't fail
        if not workflow_failed:
            self.state_manager.set_workflow_status(workflow_id, "COMPLETED", flow.name)
        return context
