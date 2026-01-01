"""
AIWork Quickstart Example
========================

This example demonstrates the basic building blocks of AIWork:
- Creating tasks with handlers
- Building a flow (workflow) with dependencies
- Executing the flow with an orchestrator

Learn more: https://github.com/JayeshCC/Aiwork/blob/main/docs/USER_GUIDE.md
"""

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator


# ═══════════════════════════════════════════════════════════════
# STEP 1: Define Task Handlers
# ═══════════════════════════════════════════════════════════════

def extract(ctx):
    """
    Extract text from a document.
    
    In a real application, this would:
    - Load a document from disk/URL
    - Use OCR for images (tesseract, OpenVINO)
    - Parse PDFs (PyPDF2, pdfplumber)
    - Return extracted text
    
    Args:
        ctx (dict): Execution context with:
            - inputs: Initial data passed to flow
            - outputs: Results from previous tasks
    
    Returns:
        dict: Extracted text data
    """
    print("    [Step 1/2] Extracting text from document...")
    
    # Simulated extraction (replace with real OCR/parsing)
    extracted_text = "Sample document content from Intel AI Challenge"
    
    print(f"    [Step 1/2] ✅ Extracted {len(extracted_text)} characters")
    
    return {"text": extracted_text}


def summarize(ctx):
    """
    Summarize extracted text.
    
    In a real application, this would:
    - Use an LLM (GPT, Claude) for summarization
    - Apply text summarization models
    - Extract key points
    
    Args:
        ctx (dict): Execution context
    
    Returns:
        dict: Summary of the text
    """
    # Access output from previous task
    text = ctx["outputs"]["extract"]["text"]
    
    print(f"    [Step 2/2] Summarizing text: '{text[:50]}...'")
    
    # Simulated summarization (replace with real model)
    summary = text[:20] + "..."
    
    print(f"    [Step 2/2] ✅ Generated summary ({len(summary)} chars)")
    
    return {"summary": summary, "original_length": len(text)}


# ═══════════════════════════════════════════════════════════════
# STEP 2: Build the Workflow
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function with error handling."""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         AIWork Quickstart Example                         ║")
    print("║         Document Processing Pipeline                      ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    try:
        # Create a flow (workflow)
        flow = Flow("document_pipeline")
        
        # Add tasks to the flow
        # Task 1: Extract text (no dependencies, runs first)
        flow.add_task(Task("extract", extract))
        
        # Task 2: Summarize (depends on extract, runs second)
        flow.add_task(Task("summarize", summarize), depends_on=["extract"])
        
        print("📋 Flow created with 2 tasks:")
        print("   1. extract → 2. summarize\n")
        
        # ═══════════════════════════════════════════════════════════
        # STEP 3: Execute the Workflow
        # ═══════════════════════════════════════════════════════════
        
        print("▶️  Starting execution...\n")
        
        # Create orchestrator (execution engine)
        orchestrator = Orchestrator()
        
        # Execute the flow with initial context
        result = orchestrator.execute(flow, {})
        
        # ═══════════════════════════════════════════════════════════
        # STEP 4: Display Results
        # ═══════════════════════════════════════════════════════════
        
        print("\n" + "═" * 60)
        print("✅ FLOW COMPLETED SUCCESSFULLY")
        print("═" * 60)
        
        print("\n📊 Final Output:")
        print(f"   • Extracted text: {result['outputs']['extract']['text'][:50]}...")
        print(f"   • Summary: {result['outputs']['summarize']['summary']}")
        print(f"   • Original length: {result['outputs']['summarize']['original_length']} chars")
        
        print("\n" + "─" * 60)
        print("💡 Next Steps:")
        print("   1. Run: python examples/memory_demo.py")
        print("   2. Explore: examples/agents/document_processor/run.py")
        print("   3. Read: docs/USER_GUIDE.md")
        print("─" * 60 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "═" * 60)
        print("❌ FLOW EXECUTION FAILED")
        print("═" * 60)
        print(f"\nError: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Check that all task handlers return dictionaries")
        print("   2. Verify dependencies are correct")
        print("   3. Ensure AIWork is installed: pip install -e .")
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
