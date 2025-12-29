from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

app = FastAPI(title="AIWork API", description="REST API for AIWork Agent Framework")

class TaskDefinition(BaseModel):
    name: str
    depends_on: List[str] = []

class FlowRequest(BaseModel):
    flow_name: str
    tasks: List[TaskDefinition]
    input_context: Dict[str, Any]

@app.get("/")
def health_check():
    return {"status": "healthy", "framework": "AIWork"}

@app.post("/execute")
def execute_flow(request: FlowRequest):
    """
    Executes a flow defined in the request.
    Note: In a real scenario, tasks would be referenced by ID or name from a registry.
    Here we just mock the execution for demonstration.
    """
    flow = Flow(request.flow_name)
    
    # Mock task creation since we can't transmit code via JSON easily in this demo
    # In production, you'd look up handlers from the ToolRegistry
    def generic_handler(ctx):
        return {"status": "executed"}

    for t_def in request.tasks:
        task = Task(t_def.name, generic_handler)
        flow.add_task(task, depends_on=t_def.depends_on)

    orchestrator = Orchestrator()
    try:
        result = orchestrator.execute(flow, request.input_context)
        return {"status": "success", "outputs": result["outputs"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
