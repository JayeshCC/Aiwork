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
    
    print(f"    [OCR] Processing document: {doc_path}")
    print("    [OCR] Using OpenVINO acceleration for fast inference...")
    
    # Simulate OpenVINO inference (in production, this runs actual model)
    ov_adapter.infer({"image": "doc_image_tensor"})
    
    # Simulated OCR result
    extracted_text = "Invoice #12345\nTotal: $5000.00\nDate: 2024-11-20\nVendor: Intel Corp"
    
    print(f"    [OCR] ✅ Successfully extracted {len(extracted_text)} characters")
    
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
    
    print("    [Analysis] Parsing invoice data...")
    
    # In production: Use NLP to extract structured data from text
    amount = 5000.00  # Parsed from "$5000.00" in text
    vendor = "Intel Corp"
    
    print(f"    [Analysis] Amount: ${amount:.2f}")
    print(f"    [Analysis] Vendor: {vendor}")
    
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
        print(f"\n    ⚠️  High-value transaction detected (${amount:.2f} > $1000)")
        print("    🔄 Triggering dynamic compliance audit...")
        
        # Create compliance audit task on-the-fly
        compliance_task = Task(
            name="audit_task",
            description="Audit the high value transaction",
            agent=compliance_agent,
            handler=lambda c: {
                "audit_status": "APPROVED",
                "reason": "Vendor is trusted",
                "auditor": "Compliance Officer",
                "timestamp": time.time()
            }
        )
        
        # Inject task into workflow
        result["next_tasks"] = [compliance_task]
        print("    ✅ Compliance audit task scheduled\n")
    else:
        print("    ℹ️  Standard transaction - no audit required\n")
    
    return result


# ═══════════════════════════════════════════════════════════════
# STEP 5: Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function with comprehensive output."""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║      AIWork Reference Agent: Document Processor           ║")
    print("║      Intelligent Invoice Processing Pipeline              ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    print("📋 Features Demonstrated:")
    print("   • Agent-Centric Architecture")
    print("   • Hybrid Orchestration (Dynamic Task Injection)")
    print("   • OpenVINO Hardware Acceleration")
    print("   • Guardrail Validation")
    print("   • Multi-Agent Collaboration\n")
    print("─" * 60 + "\n")

    try:
        # ═══════════════════════════════════════════════════════════
        # Define Flow with Multi-Agent Tasks
        # ═══════════════════════════════════════════════════════════
        
        print("🔧 Building invoice processing pipeline...\n")
        
        flow = Flow("finance_pipeline")

        # Task 1: OCR Extraction (with guardrail validation)
        task1 = Task(
            name="ocr_task",
            description="Extract text and amounts from invoice image",
            agent=ocr_agent,
            handler=ocr_extract,
            guardrails=[amount_guardrail]  # Validate extracted data
        )
        print("   1. ✅ OCR Task (Agent: Document Processor)")
        
        # Task 2: Financial Analysis (with dynamic task injection)
        task2 = Task(
            name="analyze_task",
            description="Analyze invoice for fraud and compliance",
            agent=analyst_agent,
            handler=analyze_finance
        )
        print("   2. ✅ Analysis Task (Agent: Financial Analyst)")
        print("      • Includes dynamic compliance task injection logic\n")

        flow.add_task(task1)
        flow.add_task(task2, depends_on=["ocr_task"])
        
        print("─" * 60 + "\n")

        # ═══════════════════════════════════════════════════════════
        # Execute Pipeline
        # ═══════════════════════════════════════════════════════════
        
        print("▶️  Executing pipeline...\n")
        
        orchestrator = Orchestrator()
        initial_context = {"input_path": "uploads/invoice_nov.pdf"}
        
        start_time = time.time()
        result = orchestrator.execute(flow, initial_context)
        end_time = time.time()

        # ═══════════════════════════════════════════════════════════
        # Display Results
        # ═══════════════════════════════════════════════════════════
        
        print("\n" + "═" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("═" * 60)
        
        print(f"\n⏱️  Total Execution Time: {end_time - start_time:.4f}s")
        
        print("\n📊 Task Outputs:\n")
        for task_name, output in result["outputs"].items():
            # Clean up output for display (remove next_tasks)
            display_out = output
            if isinstance(output, dict) and "next_tasks" in output:
                display_out = {k: v for k, v in output.items() if k != "next_tasks"}
            
            print(f"   {task_name}:")
            for key, value in display_out.items():
                if isinstance(value, str) and len(value) > 60:
                    print(f"      • {key}: {value[:60]}...")
                else:
                    print(f"      • {key}: {value}")
            print()
        
        print("─" * 60)
        print("💡 Key Takeaways:")
        print("   • Hybrid orchestration enables adaptive workflows")
        print("   • Agents collaborate to process complex documents")
        print("   • Guardrails ensure data quality at each step")
        print("   • OpenVINO provides hardware acceleration")
        
        print("\n" + "─" * 60)
        print("📚 Next Steps:")
        print("   1. Read: examples/agents/document_processor/README.md")
        print("   2. Customize: Adapt for your document types")
        print("   3. Explore: examples/agents/customer_support/run.py")
        print("─" * 60 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "═" * 60)
        print("❌ PIPELINE EXECUTION FAILED")
        print("═" * 60)
        print(f"\nError: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Verify all agents are properly configured")
        print("   2. Check that guardrails return boolean values")
        print("   3. Ensure task dependencies are correct")
        print("   4. Review examples/agents/document_processor/README.md")
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
