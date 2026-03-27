"""
AIWork Document Processor Agent
================================

This example demonstrates a sophisticated document processing pipeline:
- OpenVINO-accelerated OCR for text extraction
- Financial data analysis and risk assessment
- Dynamic task injection (hybrid orchestration)
- Guardrail validation for data quality
- Multi-agent collaboration

Learn more: examples/agents/document_processor/README.md
"""

import time

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.core.agent import Agent
from aiwork.core.guardrail import Guardrail
from aiwork.orchestrator import Orchestrator
from aiwork.integrations.openvino_adapter import OpenVINOAdapter


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
WHITE = "\033[97m"


def color(text, tone):
    return f"{tone}{text}{RESET}"


def section(title, tone=CYAN):
    print(color(f"\n{title}", BOLD + tone))


def agent_line(agent, action, tone=BLUE):
    print(color(f"    [{agent.role}] {action}", tone))


def progress(steps, tone=GREEN, delay=0.06):
    total = len(steps)
    width = 20
    for index, step in enumerate(steps, start=1):
        filled = int(width * index / total)
        bar = "█" * filled + "░" * (width - filled)
        print(
            f"    {color(bar, tone)} {color(f'{int(index / total * 100):>3}%', BOLD + tone)}"
            f" {step}"
        )
        time.sleep(delay)


# ═══════════════════════════════════════════════════════════════
# STEP 1: Initialize OpenVINO Adapter (Tool)
# ═══════════════════════════════════════════════════════════════

# OpenVINO provides hardware-accelerated inference for AI models
# In production, replace with actual model path
ov_adapter = OpenVINOAdapter(model_path="models/ocr_model.xml")


# ═══════════════════════════════════════════════════════════════
# STEP 2: Define Guardrails for Data Validation
# ═══════════════════════════════════════════════════════════════

def validate_positive_amount(data):
    """
    Validates that extracted data contains currency information.
    
    In production, this would:
    - Parse actual amounts from text
    - Verify amounts are positive
    - Check for valid currency formats
    
    Args:
        data (dict): Task output data
    
    Returns:
        bool: True if validation passes
    """
    return "$" in data.get("raw_text", "")


amount_guardrail = Guardrail(
    name="positive_amount_check",
    validator=validate_positive_amount,
    description="Ensures the output contains a currency symbol."
)


# ═══════════════════════════════════════════════════════════════
# STEP 3: Define Specialized Agents
# ═══════════════════════════════════════════════════════════════

ocr_agent = Agent(
    role="Document Processor",
    goal="Extract accurate text from documents using OpenVINO",
    backstory="An optimized AI specialist running on Intel hardware with 99.2% OCR accuracy.",
    tools=[ov_adapter]  # Equipped with OpenVINO for fast inference
)

analyst_agent = Agent(
    role="Financial Analyst",
    goal="Analyze financial data and ensure compliance",
    backstory="A veteran accountant with 15 years of experience who spots irregularities."
)

compliance_agent = Agent(
    role="Compliance Officer",
    goal="Audit high-value transactions for regulatory compliance",
    backstory="Strict enforcer of company policy and regulatory requirements."
)


# ═══════════════════════════════════════════════════════════════
# STEP 4: Define Task Handlers (Agent Skills)
# ═══════════════════════════════════════════════════════════════

def ocr_extract(ctx):
    """
    Extract text from invoice using OpenVINO-optimized OCR.
    
    In production, this would:
    - Load invoice image from path
    - Preprocess image (resize, denoise)
    - Run OpenVINO inference for 3.7x speedup
    - Post-process OCR results
    
    Args:
        ctx (dict): Execution context with input_path
    
    Returns:
        dict: Extracted raw text
    """
    doc_path = ctx.get("input_path", "invoice.pdf")

    section("  Stage 1: OCR Extraction", CYAN)
    agent_line(ocr_agent, f"Received document path: {doc_path}")
    progress(
        [
            "Loading invoice image",
            "Normalizing scan",
            "Running OpenVINO inference",
            "Assembling extracted text",
        ],
        tone=CYAN,
    )
    
    # Simulate OpenVINO inference (in production, this runs actual model)
    ov_adapter.infer({"image": "doc_image_tensor"})
    
    # Simulated OCR result
    extracted_text = "Invoice #12345\nTotal: $5000.00\nDate: 2024-11-20\nVendor: Intel Corp"
    
    print(color(f"    OCR complete: extracted {len(extracted_text)} characters", GREEN))
    
    return {"raw_text": extracted_text}


def analyze_finance(ctx):
    """
    Analyze invoice data and trigger compliance checks for high-value transactions.
    
    This demonstrates HYBRID ORCHESTRATION: the agent dynamically decides
    whether to inject additional tasks based on business logic.
    
    Args:
        ctx (dict): Execution context with OCR results
    
    Returns:
        dict: Analysis results and optional next_tasks for dynamic injection
    """
    text = ctx["outputs"]["ocr_task"]["raw_text"]
    
    section("  Stage 2: Financial Analysis", BLUE)
    agent_line(analyst_agent, f"Reviewing OCR payload ({len(text)} chars)", BLUE)
    progress(
        [
            "Parsing invoice fields",
            "Extracting amount and vendor",
            "Scoring transaction risk",
        ],
        tone=BLUE,
    )
    
    # In production: Use NLP to extract structured data from text
    amount = 5000.00  # Parsed from "$5000.00" in text
    vendor = "Intel Corp"
    
    print(color(f"    Amount detected: ${amount:.2f}", WHITE))
    print(color(f"    Vendor detected: {vendor}", WHITE))
    
    result = {
        "analysis": "Invoice data extracted successfully",
        "amount": amount,
        "vendor": vendor,
        "risk_score": 0.15  # Low risk
    }
    
    # ═══════════════════════════════════════════════════════════
    # KEY FEATURE: Dynamic Task Injection (Hybrid Orchestration)
    # ═══════════════════════════════════════════════════════════
    
    # Business rule: Transactions > $1000 require compliance audit
    if amount > 1000:
        print(color(f"\n    High-value transaction detected (${amount:.2f} > $1000)", YELLOW))
        agent_line(compliance_agent, "Compliance review requested dynamically", MAGENTA)
        progress(
            [
                "Creating compliance task",
                "Injecting task into execution queue",
            ],
            tone=MAGENTA,
            delay=0.05,
        )
        
        # Create compliance audit task on-the-fly
        compliance_task = Task(
            name="audit_task",
            description="Audit the high value transaction",
            agent=compliance_agent,
            handler=run_compliance_audit
        )
        
        # Inject task into workflow
        result["next_tasks"] = [compliance_task]
        print(color("    Compliance audit task scheduled", GREEN) + "\n")
    else:
        print(color("    Standard transaction - no audit required", DIM + WHITE) + "\n")
    
    return result


def run_compliance_audit(ctx):
    """Simulate compliance review for the dynamically injected task."""
    section("  Stage 3: Compliance Audit", MAGENTA)
    agent_line(compliance_agent, "Reviewing vendor trust profile and policy threshold", MAGENTA)
    progress(
        [
            "Checking approval rules",
            "Comparing against threshold",
            "Recording audit decision",
        ],
        tone=MAGENTA,
    )
    return {
        "audit_status": "APPROVED",
        "reason": "Vendor is trusted",
        "auditor": "Compliance Officer",
        "timestamp": time.time()
    }


# ═══════════════════════════════════════════════════════════════
# STEP 5: Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function with comprehensive output."""
    
    print(color("╔═══════════════════════════════════════════════════════════╗", BOLD + CYAN))
    print(color("║      AIWork Reference Agent: Document Processor           ║", BOLD + CYAN))
    print(color("║      Intelligent Invoice Processing Pipeline              ║", BOLD + CYAN))
    print(color("╚═══════════════════════════════════════════════════════════╝\n", BOLD + CYAN))

    print(color("Features Demonstrated:", BOLD + WHITE))
    print(color("   • Agent-Centric Architecture", WHITE))
    print(color("   • Hybrid Orchestration (Dynamic Task Injection)", WHITE))
    print(color("   • OpenVINO Hardware Acceleration", WHITE))
    print(color("   • Guardrail Validation", WHITE))
    print(color("   • Multi-Agent Collaboration\n", WHITE))
    print("─" * 60 + "\n")

    try:
        # ═══════════════════════════════════════════════════════════
        # Define Flow with Multi-Agent Tasks
        # ═══════════════════════════════════════════════════════════
        
        section("Building invoice processing pipeline...", CYAN)
        progress(
            [
                "Loading OCR specialist",
                "Loading financial analyst",
                "Registering compliance officer",
                "Constructing finance flow",
            ],
            tone=GREEN,
            delay=0.05,
        )
        print()
        
        flow = Flow("finance_pipeline")

        # Task 1: OCR Extraction (with guardrail validation)
        task1 = Task(
            name="ocr_task",
            description="Extract text and amounts from invoice image",
            agent=ocr_agent,
            handler=ocr_extract,
            guardrails=[amount_guardrail]  # Validate extracted data
        )
        print(color("   1. OCR Task ready        Agent: Document Processor", GREEN))
        
        # Task 2: Financial Analysis (with dynamic task injection)
        task2 = Task(
            name="analyze_task",
            description="Analyze invoice for fraud and compliance",
            agent=analyst_agent,
            handler=analyze_finance
        )
        print(color("   2. Analysis Task ready   Agent: Financial Analyst", GREEN))
        print(color("      Dynamic compliance task injection enabled\n", DIM + WHITE))

        flow.add_task(task1)
        flow.add_task(task2, depends_on=["ocr_task"])
        
        print("─" * 60 + "\n")

        # ═══════════════════════════════════════════════════════════
        # Execute Pipeline
        # ═══════════════════════════════════════════════════════════
        
        section("Executing pipeline...", GREEN)
        
        orchestrator = Orchestrator()
        initial_context = {"input_path": "uploads/invoice_nov.pdf"}
        
        start_time = time.time()
        result = orchestrator.execute(flow, initial_context)
        end_time = time.time()

        # ═══════════════════════════════════════════════════════════
        # Display Results
        # ═══════════════════════════════════════════════════════════
        
        print("\n" + "═" * 60)
        print(color("PIPELINE COMPLETED SUCCESSFULLY", BOLD + GREEN))
        print("═" * 60)

        print(color(f"\nTotal Execution Time: {end_time - start_time:.4f}s", WHITE))

        print(color("\nTask Outputs:\n", BOLD + WHITE))
        for task_name, output in result["outputs"].items():
            # Clean up output for display (remove next_tasks)
            display_out = output
            if isinstance(output, dict) and "next_tasks" in output:
                display_out = {k: v for k, v in output.items() if k != "next_tasks"}
            
            print(color(f"   {task_name}:", BOLD + CYAN))
            for key, value in display_out.items():
                if isinstance(value, str) and len(value) > 60:
                    print(color(f"      • {key}: {value[:60]}...", WHITE))
                else:
                    print(color(f"      • {key}: {value}", WHITE))
            print()
        
        print("─" * 60)
        print(color("Key Takeaways:", BOLD + WHITE))
        print(color("   • Hybrid orchestration enables adaptive workflows", WHITE))
        print(color("   • Agents collaborate to process complex documents", WHITE))
        print(color("   • Guardrails ensure data quality at each step", WHITE))
        print(color("   • OpenVINO provides hardware acceleration", WHITE))
        
        print("\n" + "─" * 60)
        print(color("Next Steps:", BOLD + WHITE))
        print(color("   1. Read: examples/agents/document_processor/README.md", WHITE))
        print(color("   2. Customize: Adapt for your document types", WHITE))
        print(color("   3. Explore: examples/agents/customer_support/run.py", WHITE))
        print("─" * 60 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "═" * 60)
        print(color("PIPELINE EXECUTION FAILED", BOLD + RED))
        print("═" * 60)
        print(color(f"\nError: {str(e)}", RED))
        print(color("\nTroubleshooting Tips:", BOLD + WHITE))
        print(color("   1. Verify all agents are properly configured", WHITE))
        print(color("   2. Check that guardrails return boolean values", WHITE))
        print(color("   3. Ensure task dependencies are correct", WHITE))
        print(color("   4. Review examples/agents/document_processor/README.md", WHITE))
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
