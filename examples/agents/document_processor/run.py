"""
Example: Document Processor Agent

To run this example, first install the aiwork package:
    pip install -e .

Then run:
    python examples/agents/document_processor/run.py
"""

import time

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.core.agent import Agent
from aiwork.core.guardrail import Guardrail
from aiwork.orchestrator import Orchestrator
from aiwork.integrations.openvino_adapter import OpenVINOAdapter

# Initialize OpenVINO Adapter (Tool)
ov_adapter = OpenVINOAdapter(model_path="models/ocr_model.xml")

# --- Guardrails ---
def validate_positive_amount(data):
    # Check if 'raw_text' contains a positive amount (simplified check)
    return "$" in data.get("raw_text", "")

amount_guardrail = Guardrail(
    name="positive_amount_check",
    validator=validate_positive_amount,
    description="Ensures the output contains a currency symbol."
)

# --- Define Agents ---

ocr_agent = Agent(
    role="Document Processor",
    goal="Extract accurate text from documents using OpenVINO",
    backstory="An optimized AI specialist running on Intel hardware.",
    tools=[ov_adapter]
)

analyst_agent = Agent(
    role="Financial Analyst",
    goal="Analyze financial data and ensure compliance",
    backstory="A veteran accountant who spots irregularities."
)

compliance_agent = Agent(
    role="Compliance Officer",
    goal="Audit high-value transactions",
    backstory="Strict enforcer of company policy."
)

# --- Define Task Handlers (Skills) ---

def ocr_extract(ctx):
    """
    Simulates OCR extraction using OpenVINO optimization.
    """
    doc_path = ctx.get("input_path", "invoice.pdf")
    # Simulate OpenVINO inference
    ov_adapter.infer({"image": "doc_image_tensor"})
    
    return {"raw_text": "Invoice #12345\nTotal: $5000.00\nDate: 2024-11-20\nVendor: Intel Corp"}

def analyze_finance(ctx):
    """
    Analyzes the text and decides if further action is needed (Hybrid Orchestration).
    """
    text = ctx["outputs"]["ocr_task"]["raw_text"]
    amount = 5000.00 # Parsed from text
    
    result = {"analysis": "High value invoice detected."}
    
    # Dynamic Decision: If amount > $1000, trigger a compliance check
    if amount > 1000:
        print("    [Agent Decision] Amount > $1000. Triggering Compliance Check.")
        
        # Create a new task dynamically
        compliance_task = Task(
            name="audit_task",
            description="Audit the high value transaction",
            agent=compliance_agent,
            handler=lambda c: {"audit_status": "APPROVED", "reason": "Vendor is trusted"}
        )
        
        result["next_tasks"] = [compliance_task]
        
    return result

def main():
    print("=== AIWork Reference Agent: Document Processor ===")
    print("Mode: Agent-Centric + Hybrid Orchestration\n")

    # Define Flow (User Defined Part)
    flow = Flow("finance_pipeline")

    # 1. OCR Task assigned to OCR Agent
    task1 = Task(
        name="ocr_task", 
        description="Read the invoice", 
        agent=ocr_agent, 
        handler=ocr_extract,
        guardrails=[amount_guardrail]
    )
    
    # 2. Analysis Task assigned to Analyst Agent
    task2 = Task(
        name="analyze_task", 
        description="Analyze for fraud", 
        agent=analyst_agent, 
        handler=analyze_finance
    )

    flow.add_task(task1)
    flow.add_task(task2, depends_on=["ocr_task"])

    # Execute
    orchestrator = Orchestrator()
    initial_context = {"input_path": "uploads/invoice_nov.pdf"}
    
    start_time = time.time()
    result = orchestrator.execute(flow, initial_context)
    end_time = time.time()

    print("\n=== Execution Results ===")
    print(f"Total Time: {end_time - start_time:.4f}s")
    print("Outputs:")
    for task_name, output in result["outputs"].items():
        # Clean up output for display
        display_out = output
        if isinstance(output, dict) and "next_tasks" in output:
            display_out = {k:v for k,v in output.items() if k != "next_tasks"}
        print(f"  {task_name}: {display_out}")

if __name__ == "__main__":
    main()
