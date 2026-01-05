import time
from typing import Any, Dict


class StateManager:
    """
    Manages workflow and task state with persistence.
    
    Tracks:
    - Workflow status (PENDING, RUNNING, COMPLETED, FAILED)
    - Task status per workflow
    - Task outputs
    - Timestamps
    - Error messages
    """
    def __init__(self, use_redis=False):
        """
        Initialize state manager.
        
        Args:
            use_redis: If True, use Redis backend (not fully implemented)
                      If False, uses in-memory dict (ephemeral)
        """
        self.use_redis = use_redis
        self.local_store = {}
        self.workflows = {}  # workflow_id -> workflow_data
        if use_redis:
            print("Initializing Redis connection for state management...")
            # self.redis = redis.Redis(...)

    def save_state(self, flow_id: str, state: dict):
        """Legacy method for backward compatibility."""
        if self.use_redis:
            # self.redis.set(flow_id, json.dumps(state))
            pass
        else:
            self.local_store[flow_id] = state

    def get_state(self, flow_id: str):
        """Legacy method for backward compatibility."""
        if self.use_redis:
            # return json.loads(self.redis.get(flow_id))
            return {}
        return self.local_store.get(flow_id, {})
    
    def set_workflow_status(self, workflow_id: str, status: str, name: str = None, error: str = None):
        """
        Update workflow status.
        
        Args:
            workflow_id: Unique identifier for the workflow
            status: Workflow status (PENDING, RUNNING, COMPLETED, FAILED)
            name: Optional workflow name
            error: Optional error message if status is FAILED
        """
        if workflow_id not in self.workflows:
            self.workflows[workflow_id] = {
                "name": name,
                "status": status,
                "tasks": {},
                "created_at": time.time(),
                "error": None
            }
        
        self.workflows[workflow_id]["status"] = status
        self.workflows[workflow_id]["updated_at"] = time.time()
        if error:
            self.workflows[workflow_id]["error"] = error
    
    def set_task_status(self, workflow_id: str, task_name: str, status: str, error: str = None):
        """
        Update task status within workflow.
        
        Args:
            workflow_id: Unique identifier for the workflow
            task_name: Name of the task
            status: Task status (PENDING, RUNNING, COMPLETED, FAILED)
            error: Optional error message if status is FAILED
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if task_name not in self.workflows[workflow_id]["tasks"]:
            self.workflows[workflow_id]["tasks"][task_name] = {
                "status": status,
                "output": None,
                "error": None,
                "started_at": time.time()
            }
        
        self.workflows[workflow_id]["tasks"][task_name]["status"] = status
        self.workflows[workflow_id]["tasks"][task_name]["updated_at"] = time.time()
        if error:
            self.workflows[workflow_id]["tasks"][task_name]["error"] = error
    
    def update_task_output(self, workflow_id: str, task_name: str, output: Any):
        """
        Store task output.
        
        Args:
            workflow_id: Unique identifier for the workflow
            task_name: Name of the task
            output: Task execution output
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if task_name not in self.workflows[workflow_id]["tasks"]:
            # Task doesn't exist yet - create with default completed status
            self.workflows[workflow_id]["tasks"][task_name] = {
                "status": "COMPLETED",
                "output": output,
                "error": None,
                "updated_at": time.time()
            }
        else:
            # Task exists - only update output, preserve existing status
            self.workflows[workflow_id]["tasks"][task_name]["output"] = output
            self.workflows[workflow_id]["tasks"][task_name]["updated_at"] = time.time()
    
    def get_workflow_state(self, workflow_id: str) -> Dict:
        """
        Retrieve complete workflow state.
        
        Args:
            workflow_id: Unique identifier for the workflow
            
        Returns:
            Dict containing workflow status, tasks, and metadata
            
        Raises:
            ValueError: If workflow_id not found
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        return self.workflows[workflow_id]
    
    def get_task_status(self, workflow_id: str, task_name: str) -> str:
        """
        Get status of specific task.
        
        Args:
            workflow_id: Unique identifier for the workflow
            task_name: Name of the task
            
        Returns:
            Task status string (PENDING, RUNNING, COMPLETED, FAILED)
        """
        state = self.get_workflow_state(workflow_id)
        if task_name not in state["tasks"]:
            return "PENDING"
        return state["tasks"][task_name]["status"]
