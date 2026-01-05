from typing import Callable, Any, Dict, Optional
import uuid
import warnings

class Task:
    """
    Atomic unit of work in the AIWork framework.
    """
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        agent: Optional['Agent'] = None,
        handler: Callable[[Dict[str, Any]], Any] = None,
        retries: int = 3,
        guardrails: list = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        # Backward compatibility: allow Task(name, handler) signature.
        if callable(description) and handler is None:
            handler = description
            description = None
        self.description = description or name
        self.agent = agent
        self.handler = handler
        self.retries = retries
        self.guardrails = guardrails or []
        self.status = "PENDING"
        self.output = None
        self.error = None

    def _run_handler(self, context: Dict[str, Any]) -> Any:
        """
        Internal method to run the task's handler or agent.
        This should be called by the executor, not directly.
        
        Args:
            context: Execution context with workflow state
            
        Returns:
            Task execution result
            
        Raises:
            ValueError: If task has no handler and no agent
        """
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
        
        return result

    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Executes the task with retry logic and guardrails.
        
        DEPRECATED: This method is deprecated. Use an Orchestrator with an Executor instead.
        The orchestrator will handle task execution through the executor pattern.
        
        This method is kept for backward compatibility and will be removed in a future version.
        """
        warnings.warn(
            "Task.execute() is deprecated. Use Orchestrator with an Executor instead. "
            "Example: orchestrator.execute(flow, context)",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Use LocalExecutor for backward compatibility
        from aiwork.executors.local_executor import LocalExecutor
        executor = LocalExecutor()
        return executor.execute(self, context)
