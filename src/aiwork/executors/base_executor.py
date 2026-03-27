from typing import TYPE_CHECKING, Any, Dict
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from aiwork.core.task import Task


class BaseExecutor(ABC):
    """
    Abstract base class for task execution strategies.

    Executors define HOW tasks run (local, remote, parallel, etc.)
    while Tasks define WHAT work to do.
    """

    @abstractmethod
    def execute(self, task: "Task", context: Dict[str, Any]) -> Any:
        """
        Execute a task with the given context.

        Args:
            task: Task to execute
            context: Execution context with workflow state

        Returns:
            Task execution result

        Raises:
            Exception: If task execution fails after all retries
        """
        pass
