from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable

class LocalExecutor:
    """
    Executes tasks locally, potentially in parallel.
    """
    def __init__(self, max_workers=4):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def execute_tasks(self, tasks: List[Callable], context):
        """
        Execute a list of tasks (that don't depend on each other) in parallel.
        """
        futures = []
        for task in tasks:
            futures.append(self.pool.submit(task, context))
        
        results = [f.result() for f in futures]
        return results
