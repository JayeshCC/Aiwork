from typing import Any, Dict, List, Callable
import time
from concurrent.futures import ThreadPoolExecutor
from .base_executor import BaseExecutor


class LocalExecutor(BaseExecutor):
    """
    Executes tasks locally with retry logic, guardrails, and metrics.
    
    This executor implements the execution strategy for running tasks
    in the local process with support for retries, error handling,
    guardrail validation, and metrics recording.
    """
    
    def __init__(self, max_workers=4):
        """
        Initialize the LocalExecutor.
        
        Args:
            max_workers: Maximum number of workers for parallel execution (reserved for future use)
        """
        self.max_workers = max_workers
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
    
    def execute(self, task: 'Task', context: Dict[str, Any]) -> Any:
        """
        Execute a task with retry logic, guardrails, and metrics.
        
        Args:
            task: Task to execute
            context: Execution context with workflow state
            
        Returns:
            Task execution result
            
        Raises:
            Exception: If task execution fails after all retries
        """
        from aiwork.core.observability import metrics
        
        task.status = "RUNNING"
        attempt = 0
        start_time = time.time()
        
        while attempt <= task.retries:
            try:
                attempt += 1
                
                # --- Input Guardrails (Future) ---
                # if task.input_guardrails: ...

                # Execute the task's core logic
                result = task._run_handler(context)

                # --- Output Guardrails ---
                if hasattr(task, 'guardrails') and task.guardrails:
                    for guard in task.guardrails:
                        if not guard.validate(result):
                            raise ValueError(f"Guardrail '{guard.name}' failed validation.")

                task.output = result
                task.status = "COMPLETED"
                
                duration = time.time() - start_time
                metrics.record("task_duration_seconds", duration, {"task": task.name, "status": "success"})
                
                return result

            except Exception as e:
                print(f"  [Task {task.name}] Attempt {attempt}/{task.retries + 1} Failed: {e}")
                if attempt > task.retries:
                    task.error = str(e)
                    task.status = "FAILED"
                    
                    duration = time.time() - start_time
                    metrics.record("task_duration_seconds", duration, {"task": task.name, "status": "failed"})
                    
                    raise e
                # Optional: Add backoff sleep here
    
    def execute_tasks(self, tasks: List[Callable], context):
        """
        Execute a list of tasks (that don't depend on each other) in parallel.
        
        This is a legacy method for backward compatibility.
        """
        futures = []
        for task in tasks:
            futures.append(self.pool.submit(task, context))
        
        results = [f.result() for f in futures]
        return results


