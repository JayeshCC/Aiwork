from typing import Dict, Any
from .core.flow import Flow

class Orchestrator:
    """
    Executes Flows, managing state and dependencies.
    """
    def __init__(self):
        self.memory = {}

    def execute(self, flow: Flow, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executes the given flow.
        """
        context = initial_context or {}
        context["outputs"] = {}
        
        # Get execution order
        try:
            execution_order = flow.get_topological_sort()
        except ValueError as e:
            print(f"Flow Error: {e}")
            return context

        print(f"Starting Flow: {flow.name}")
        
        # We use a list that can be dynamically appended to
        execution_queue = list(execution_order)
        processed_tasks = set()

        i = 0
        while i < len(execution_queue):
            task = execution_queue[i]
            i += 1
            
            if task.name in processed_tasks:
                continue

            print(f"  Executing Task: {task.name}...")
            if hasattr(task, 'agent') and task.agent:
                 print(f"    > Assigned to Agent: {task.agent.role}")

            try:
                # Pass the full context to the task
                result = task.execute(context)
                context["outputs"][task.name] = result
                processed_tasks.add(task.name)
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
                # In a real system, handle retries or stop flow
                break
        
        print(f"Flow {flow.name} Finished.")
        return context
