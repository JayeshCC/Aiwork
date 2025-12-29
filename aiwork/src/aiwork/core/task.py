from typing import Callable, Any, Dict, Optional
import uuid

class Task:
    """
    Atomic unit of work in the AIWork framework.
    """
    def __init__(self, name: str, description: str, agent: Optional['Agent'] = None, handler: Callable[[Dict[str, Any]], Any] = None, retries: int = 3, guardrails: list = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.agent = agent
        self.handler = handler
        self.retries = retries
        self.guardrails = guardrails or []
        self.status = "PENDING"
        self.output = None
        self.error = None

    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Executes the task with retry logic and guardrails.
        """
        from aiwork.core.observability import metrics
        import time
        
        self.status = "RUNNING"
        attempt = 0
        start_time = time.time()
        
        while attempt <= self.retries:
            try:
                attempt += 1
                
                # --- Input Guardrails (Future) ---
                # if self.input_guardrails: ...

                if self.agent:
                    # Agent-centric execution
                    if self.handler:
                        result = self.handler(context)
                    else:
                        result = self.agent.execute_task(self.description, context)
                elif self.handler:
                    # Legacy/Function-centric execution
                    result = self.handler(context)
                else:
                    raise ValueError(f"Task {self.name} has no Agent and no Handler.")

                # --- Output Guardrails ---
                if hasattr(self, 'guardrails') and self.guardrails:
                    for guard in self.guardrails:
                        if not guard.validate(result):
                            raise ValueError(f"Guardrail '{guard.name}' failed validation.")

                self.output = result
                self.status = "COMPLETED"
                
                duration = time.time() - start_time
                metrics.record("task_duration_seconds", duration, {"task": self.name, "status": "success"})
                
                return result

            except Exception as e:
                print(f"  [Task {self.name}] Attempt {attempt}/{self.retries + 1} Failed: {e}")
                if attempt > self.retries:
                    self.error = str(e)
                    self.status = "FAILED"
                    
                    duration = time.time() - start_time
                    metrics.record("task_duration_seconds", duration, {"task": self.name, "status": "failed"})
                    
                    raise e
                # Optional: Add backoff sleep here

