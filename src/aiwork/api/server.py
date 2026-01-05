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

app = Flask(__name__)

# In-memory storage for workflows and tasks
workflow_store: Dict[str, Dict[str, Any]] = {}
task_store: Dict[str, Dict[str, Any]] = {}

# Thread lock for thread-safe access to stores
store_lock = threading.Lock()


def execute_workflow_async(workflow_id: str, flow: Flow, initial_context: Dict[str, Any]):
    """
    Execute a workflow asynchronously and update the workflow store with results.
    """
    try:
        # Update status to RUNNING
        with store_lock:
            if workflow_id not in workflow_store:
                return
            workflow_store[workflow_id]["status"] = "RUNNING"
        
        # Execute workflow (this is the long-running operation)
        orchestrator = Orchestrator()
        result = orchestrator.execute(flow, initial_context)
        
        # Update workflow status to COMPLETED
        with store_lock:
            if workflow_id not in workflow_store:
                return
            workflow_store[workflow_id]["status"] = "COMPLETED"
            workflow_store[workflow_id]["result"] = result
            
            # Store individual task results
            if "outputs" in result:
                for task_name, task_output in result["outputs"].items():
                    # Find the task object to get its ID and other metadata
                    if task_name in flow.tasks:
                        task_obj = flow.tasks[task_name]
                        task_store[task_obj.id] = {
                            "id": task_obj.id,
                            "name": task_obj.name,
                            "status": task_obj.status,
                            "output": task_obj.output,
                            "error": task_obj.error
                        }
    
    except Exception as e:
        # Update workflow status to FAILED
        with store_lock:
            if workflow_id in workflow_store:
                workflow_store[workflow_id]["status"] = "FAILED"
                workflow_store[workflow_id]["error"] = str(e)


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
        
        # Store workflow
        workflow_store[workflow_id] = {
            "id": workflow_id,
            "name": workflow_name,
            "flow": flow,
            "status": "PENDING",
            "result": None,
            "error": None
        }
        
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
    Check workflow execution status.
    
    Returns:
    {
        "id": "workflow-uuid",
        "name": "workflow_name",
        "status": "PENDING|RUNNING|COMPLETED|FAILED",
        "outputs": {},  # Present if COMPLETED
        "error": ""     # Present if FAILED
    }
    """
    with store_lock:
        if workflow_id not in workflow_store:
            return jsonify({
                "error": f"Workflow {workflow_id} not found"
            }), 404
        
        workflow = workflow_store[workflow_id]
        
        response = {
            "id": workflow["id"],
            "name": workflow["name"],
            "status": workflow["status"]
        }
        
        if workflow["status"] == "COMPLETED" and workflow["result"]:
            response["outputs"] = workflow["result"].get("outputs", {})
        
        if workflow["status"] == "FAILED" and workflow["error"]:
            response["error"] = workflow["error"]
    
    return jsonify(response), 200


@app.route("/task/<task_id>", methods=["GET"])
def get_task_result(task_id: str):
    """
    Get individual task result.
    
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


def start_server():
    """
    Start the Flask server on port 5000.
    """
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    start_server()
