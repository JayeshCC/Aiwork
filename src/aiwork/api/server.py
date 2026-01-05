"""
REST API Server for AIWork Framework

This module provides a Flask-based REST API for workflow submission and monitoring.
It implements the explicit execution pipeline: Ingress → Orchestrator → Executors

To start the server:
    python -m aiwork.api.server
    
Or use the command:
    aiwork-server

The server will run on http://localhost:5000

Endpoints:
    POST /workflow - Submit a new workflow for execution
    GET /workflow/{id} - Check workflow execution status
    GET /task/{id} - Get individual task result
    GET /health - Health check endpoint

IMPORTANT NOTES FOR PRODUCTION:
    - This is a demonstration server, NOT intended for production use
    - Uses in-memory storage (data lost on restart)
    - Binds to 0.0.0.0 for demonstration (use 127.0.0.1 or configure for production)
    - Daemon threads may be forcibly killed on shutdown (use proper thread pool in production)
    - No authentication or rate limiting implemented
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import uuid
import threading
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator
from aiwork.memory.state_manager import StateManager

app = Flask(__name__)

# Shared StateManager and Orchestrator for all workflows
state_manager = StateManager()
orchestrator = Orchestrator(state_manager=state_manager)

# In-memory storage for workflows and tasks (kept for backward compatibility)
workflow_store: Dict[str, Dict[str, Any]] = {}
task_store: Dict[str, Dict[str, Any]] = {}

# Thread lock for thread-safe access to stores
store_lock = threading.Lock()


def execute_workflow_async(workflow_id: str, flow: Flow, initial_context: Dict[str, Any]):
    """
    Execute a workflow asynchronously using shared orchestrator with StateManager.
    """
    try:
        # Execute workflow (this is the long-running operation)
        # Pass the workflow_id so orchestrator uses it for tracking
        orchestrator.execute(flow, initial_context, workflow_id=workflow_id)
    
    except Exception as e:
        # Error tracking is already handled by orchestrator's StateManager
        # Just log for debugging
        print(f"Workflow execution error: {e}")


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    Returns the status of the API server.
    """
    return jsonify({
        "status": "healthy",
        "framework": "AIWork",
        "version": "0.1.0"
    }), 200


@app.route("/workflow", methods=["POST"])
def submit_workflow():
    """
    Submit a new workflow for execution.
    
    Request body should contain:
    {
        "name": "workflow_name",
        "tasks": [
            {
                "name": "task1",
                "depends_on": []
            }
        ],
        "context": {}  # Optional initial context
    }
    
    Returns:
    {
        "id": "workflow-uuid",
        "status": "PENDING"
    }
    """
    try:
        data = request.get_json()
        
        if not data or "name" not in data or "tasks" not in data:
            return jsonify({
                "error": "Invalid request. 'name' and 'tasks' are required."
            }), 400
        
        workflow_name = data["name"]
        tasks_data = data["tasks"]
        initial_context = data.get("context", {})
        
        # Create workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Create Flow
        flow = Flow(workflow_name)
        
        # Generic handler for tasks (in production, look up from registry)
        def generic_handler(ctx):
            return {"status": "executed"}
        
        # Add tasks to flow
        for task_data in tasks_data:
            task_name = task_data.get("name")
            depends_on = task_data.get("depends_on", [])
            
            if not task_name:
                return jsonify({
                    "error": "Each task must have a 'name' field."
                }), 400
            
            task = Task(task_name, generic_handler)
            flow.add_task(task, depends_on=depends_on)
        
        # Initialize workflow state in StateManager
        state_manager.set_workflow_status(workflow_id, "PENDING", workflow_name)
        
        # Execute workflow asynchronously
        thread = threading.Thread(
            target=execute_workflow_async,
            args=(workflow_id, flow, initial_context)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "id": workflow_id,
            "status": "PENDING",
            "message": "Workflow submitted successfully"
        }), 201
    
    except Exception as e:
        return jsonify({
            "error": f"Failed to submit workflow: {str(e)}"
        }), 500


@app.route("/workflow/<workflow_id>", methods=["GET"])
def get_workflow_status(workflow_id: str):
    """
    Check workflow execution status from StateManager.
    
    Returns:
    {
        "id": "workflow-uuid",
        "name": "workflow_name",
        "status": "PENDING|RUNNING|COMPLETED|FAILED",
        "tasks": {
            "task_name": {
                "status": "COMPLETED",
                "output": {...}
            }
        },
        "error": ""     # Present if FAILED
    }
    """
    try:
        state = state_manager.get_workflow_state(workflow_id)
        
        response = {
            "id": workflow_id,
            "name": state["name"],
            "status": state["status"],
            "tasks": state["tasks"]
        }
        
        if state.get("error"):
            response["error"] = state["error"]
        
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify({
            "error": f"Workflow {workflow_id} not found"
        }), 404


@app.route("/task/<task_id>", methods=["GET"])
def get_task_result(task_id: str):
    """
    Get individual task result (legacy endpoint using task_store).
    
    Note: This endpoint is for backward compatibility.
    Use /workflow/<workflow_id>/task/<task_name> for new integrations.
    
    Returns:
    {
        "id": "task-uuid",
        "name": "task_name",
        "status": "PENDING|RUNNING|COMPLETED|FAILED",
        "output": {},   # Present if COMPLETED
        "error": ""     # Present if FAILED
    }
    """
    with store_lock:
        if task_id not in task_store:
            return jsonify({
                "error": f"Task {task_id} not found"
            }), 404
        
        task = task_store[task_id]
    
    return jsonify(task), 200


@app.route("/workflow/<workflow_id>/task/<task_name>", methods=["GET"])
def get_task_status(workflow_id: str, task_name: str):
    """
    Get status of specific task within a workflow from StateManager.
    
    Returns:
    {
        "workflow_id": "...",
        "task_name": "...",
        "status": "PENDING|RUNNING|COMPLETED|FAILED",
        "output": {...},
        "error": "..."
    }
    """
    try:
        status = state_manager.get_task_status(workflow_id, task_name)
        state = state_manager.get_workflow_state(workflow_id)
        task_data = state["tasks"].get(task_name, {})
        
        return jsonify({
            "workflow_id": workflow_id,
            "task_name": task_name,
            "status": status,
            "output": task_data.get("output"),
            "error": task_data.get("error")
        }), 200
    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404


def start_server():
    """
    Start the Flask server on port 5000.
    """
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    start_server()
