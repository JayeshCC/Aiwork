from typing import List, Dict, Set
from .task import Task

class Flow:
    """
    Represents a workflow as a Directed Acyclic Graph (DAG) of tasks.
    """
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.dependencies: Dict[str, Set[str]] = {}  # task_name -> set of dependency_names

    def add_task(self, task: Task, depends_on: List[str] = None):
        """
        Adds a task to the flow with optional dependencies.
        """
        if task.name in self.tasks:
            raise ValueError(f"Task with name {task.name} already exists in flow.")
        
        self.tasks[task.name] = task
        self.dependencies[task.name] = set(depends_on) if depends_on else set()

        # Validate dependencies exist
        for dep in self.dependencies[task.name]:
            if dep not in self.tasks:
                # In a real implementation, we might allow adding deps later, 
                # but for simplicity, we enforce order or check at execution.
                pass 

    def get_topological_sort(self) -> List[Task]:
        """
        Returns a list of tasks in topological order for execution.
        """
        visited = set()
        temp_mark = set()
        sorted_tasks = []

        def visit(n: str):
            if n in temp_mark:
                raise ValueError("Cycle detected in Flow DAG")
            if n not in visited:
                temp_mark.add(n)
                for m in self.tasks:
                    if n in self.dependencies[m]: # if m depends on n (reverse check for standard topo sort usually goes by edges)
                        # My dependency structure is: task -> [deps]. 
                        # So if I want to execute deps first, I visit deps first.
                        pass
                
                # Let's use a standard algorithm based on my structure
                # Visit all dependencies first
                for dep_name in self.dependencies[n]:
                    visit(dep_name)
                
                temp_mark.remove(n)
                visited.add(n)
                sorted_tasks.append(self.tasks[n])

        for task_name in self.tasks:
            if task_name not in visited:
                visit(task_name)
        
        return sorted_tasks
