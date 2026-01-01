import sys
import os

# Add src to path so we can import aiwork without installing it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

# Define tasks
def extract(ctx):
    print("    [Logic] Extracting text from document...")
    return {"text": "Sample document content from Intel AI Challenge"}

def summarize(ctx):
    text = ctx["outputs"]["extract"]["text"]
    print(f"    [Logic] Summarizing text: '{text}'")
    return {"summary": text[:20] + "..."}

def main():
    # Build flow
    flow = Flow("document_pipeline")
    
    # Add tasks
    # Note: In this basic version, we add tasks and then define dependencies
    # The 'depends_on' argument in add_task handles the DAG connection
    flow.add_task(Task("extract", extract))
    flow.add_task(Task("summarize", summarize), depends_on=["extract"])

    # Execute
    orchestrator = Orchestrator()
    result = orchestrator.execute(flow, {})
    
    print("\nFinal Output:")
    print(result["outputs"])

if __name__ == "__main__":
    main()
