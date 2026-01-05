from typing import Any, Dict, List, Callable
import time
from concurrent.futures import ThreadPoolExecutor
from aiwork.core.observability import metrics
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
            max_workers: Maximum number of workers for parallel execution.
                        Used by execute_tasks() for backward compatibility.
        """
        self.max_workers = max_workers
        # ThreadPoolExecutor is used by the legacy execute_tasks() method
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
        task.status = "RUNNING"
        attempt = 0
        start_time = time.time()
        
        # Check if task has verbose mode enabled
        verbose = getattr(task, 'verbose', False)
        
        while attempt <= task.retries:
            try:
                attempt += 1
                
                # --- Input Guardrails ---
                input_guardrails = getattr(task, 'input_guardrails', [])
                if input_guardrails:
                    if verbose:
                        print(f"    [Task {task.name}] Validating input with {len(input_guardrails)} guardrails...")
                    
                    for guard in input_guardrails:
                        if not guard.validate(context):
                            error_msg = f"Input guardrail '{guard.name}' failed validation"
                            if verbose:
                                print(f"    [Task {task.name}] ❌ {error_msg}")
                            raise ValueError(error_msg)
                    
                    if verbose:
                        print(f"    [Task {task.name}] ✅ Input validation passed")

                # Execute the task's core logic
                result = task._run_handler(context)

                # --- Output Guardrails ---
                output_guardrails = getattr(task, 'guardrails', [])
                if output_guardrails:
                    if verbose:
                        print(f"    [Task {task.name}] Validating output with {len(output_guardrails)} guardrails...")
                    
                    for guard in output_guardrails:
                        if not guard.validate(result):
                            error_msg = f"Output guardrail '{guard.name}' failed validation"
                            if verbose:
                                print(f"    [Task {task.name}] ❌ {error_msg}")
                            raise ValueError(error_msg)
                    
                    if verbose:
                        print(f"    [Task {task.name}] ✅ Output validation passed")

                task.output = result
                task.status = "COMPLETED"
                
                duration = time.time() - start_time
                # Metrics use "success"/"failed" labels (not task status values)
                # to maintain compatibility with monitoring systems
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


