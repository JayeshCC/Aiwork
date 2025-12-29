import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

def understand_intent(ctx):
    query = ctx.get("query", "")
    print(f"  [Bot] Analyzing intent for: '{query}'")
    # Simple keyword matching for demo
    if "refund" in query.lower():
        return {"intent": "refund_request", "confidence": 0.95}
    elif "hours" in query.lower():
        return {"intent": "check_hours", "confidence": 0.98}
    return {"intent": "general_inquiry", "confidence": 0.8}

def search_knowledge_base(ctx):
    intent = ctx["outputs"]["intent"]["intent"]
    print(f"  [Bot] Searching KB for intent: {intent}")
    
    kb = {
        "refund_request": "Refunds are processed within 3-5 business days.",
        "check_hours": "We are open Mon-Fri, 9am-5pm EST.",
        "general_inquiry": "Please contact support@example.com for more info."
    }
    return {"kb_result": kb.get(intent, "No info found.")}

def generate_response(ctx):
    kb_result = ctx["outputs"]["search"]["kb_result"]
    print("  [Bot] Generating final response...")
    return {"response": f"Here is the information you requested: {kb_result}"}

def main():
    print("=== AIWork Reference Agent: Customer Support Bot ===")
    
    # Define Flow
    flow = Flow("support_bot_v1")
    
    flow.add_task(Task("intent", understand_intent))
    flow.add_task(Task("search", search_knowledge_base), depends_on=["intent"])
    flow.add_task(Task("respond", generate_response), depends_on=["search"])

    # Execute
    orchestrator = Orchestrator()
    
    # Test Case 1
    print("\n--- User Query: 'I want a refund' ---")
    ctx1 = {"query": "I want a refund for my last order"}
    res1 = orchestrator.execute(flow, ctx1)
    print(f"Bot: {res1['outputs']['respond']['response']}")

    # Test Case 2
    print("\n--- User Query: 'What are your hours?' ---")
    ctx2 = {"query": "What are your opening hours?"}
    # Re-instantiate flow or reset? 
    # In this simple design, we can reuse the flow definition but state is in context.
    # However, the Orchestrator execute method resets context outputs.
    res2 = orchestrator.execute(flow, ctx2)
    print(f"Bot: {res2['outputs']['respond']['response']}")

if __name__ == "__main__":
    main()
