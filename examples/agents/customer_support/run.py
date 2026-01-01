"""
AIWork Customer Support Agent
==============================

This example demonstrates an intelligent customer support bot:
- Intent classification for query understanding
- Knowledge base search for relevant information
- Context-aware response generation
- Multi-turn conversation handling

Learn more: examples/agents/customer_support/README.md
"""

import time

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator


# ═══════════════════════════════════════════════════════════════
# STEP 1: Define Intent Classification Handler
# ═══════════════════════════════════════════════════════════════

def understand_intent(ctx):
    """
    Classify customer query intent using keyword matching.
    
    In production, this would:
    - Use ML models (BERT, transformers) for classification
    - Support multi-intent queries
    - Handle misspellings and variations
    - Return confidence scores
    
    Args:
        ctx (dict): Context with customer query
    
    Returns:
        dict: Detected intent and confidence score
    """
    query = ctx.get("query", "")
    
    print(f"    [Intent] Analyzing query: '{query}'")
    print("    [Intent] Running classification model...")
    
    # Simple keyword-based classification (replace with ML model)
    query_lower = query.lower()
    
    if "refund" in query_lower or "money back" in query_lower:
        intent = "refund_request"
        confidence = 0.95
        print(f"    [Intent] ✅ Detected: REFUND_REQUEST (confidence: {confidence})")
    elif "hours" in query_lower or "open" in query_lower or "schedule" in query_lower:
        intent = "check_hours"
        confidence = 0.98
        print(f"    [Intent] ✅ Detected: CHECK_HOURS (confidence: {confidence})")
    else:
        intent = "general_inquiry"
        confidence = 0.80
        print(f"    [Intent] ✅ Detected: GENERAL_INQUIRY (confidence: {confidence})")
    
    return {
        "intent": intent,
        "confidence": confidence,
        "original_query": query
    }


# ═══════════════════════════════════════════════════════════════
# STEP 2: Define Knowledge Base Search Handler
# ═══════════════════════════════════════════════════════════════

def search_knowledge_base(ctx):
    """
    Search knowledge base for relevant information based on intent.
    
    In production, this would:
    - Use vector search (FAISS, Pinecone) for semantic matching
    - Rank results by relevance
    - Handle multi-document retrieval
    - Include metadata (source, date, author)
    
    Args:
        ctx (dict): Context with detected intent
    
    Returns:
        dict: Knowledge base search results
    """
    intent = ctx["outputs"]["intent"]["intent"]
    
    print(f"    [Search] Searching knowledge base for: {intent}")
    print("    [Search] Running vector similarity search...")
    
    # Simulated knowledge base (replace with real vector DB)
    kb = {
        "refund_request": "Refunds are processed within 3-5 business days. Please provide your order number and reason for the refund request.",
        "check_hours": "We are open Monday-Friday, 9am-5pm EST. Weekend hours: Saturday 10am-3pm. Closed on Sundays and major holidays.",
        "general_inquiry": "For general inquiries, please contact support@example.com or call 1-800-SUPPORT. Our team typically responds within 24 hours."
    }
    
    result = kb.get(intent, "No relevant information found.")
    
    print(f"    [Search] ✅ Found relevant information ({len(result)} chars)")
    
    return {
        "kb_result": result,
        "source": "knowledge_base_v2",
        "relevance_score": 0.92
    }


# ═══════════════════════════════════════════════════════════════
# STEP 3: Define Response Generation Handler
# ═══════════════════════════════════════════════════════════════

def generate_response(ctx):
    """
    Generate personalized response combining KB information and query context.
    
    In production, this would:
    - Use LLM (GPT-4, Claude) for natural language generation
    - Incorporate conversation history
    - Add personalization based on user profile
    - Include follow-up suggestions
    
    Args:
        ctx (dict): Context with KB results and intent
    
    Returns:
        dict: Generated response
    """
    kb_result = ctx["outputs"]["search"]["kb_result"]
    
    # Get intent and confidence if available (may not be in test scenarios)
    intent = None
    confidence = None
    if "intent" in ctx["outputs"]:
        intent = ctx["outputs"]["intent"]["intent"]
        confidence = ctx["outputs"]["intent"]["confidence"]
    
    print("    [Response] Generating personalized response...")
    print("    [Response] Using LLM for natural language generation...")
    
    # Simple template-based response (replace with LLM)
    response = f"Here is the information you requested: {kb_result}"
    
    print(f"    [Response] ✅ Generated response ({len(response)} chars)")
    
    result = {
        "response": response,
        "follow_up_suggestions": [
            "Is there anything else I can help you with?",
            "Would you like to speak with a human agent?"
        ]
    }
    
    # Add intent and confidence if available
    if intent is not None:
        result["intent"] = intent
    if confidence is not None:
        result["confidence"] = confidence
    
    return result


# ═══════════════════════════════════════════════════════════════
# STEP 4: Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function demonstrating multi-query support bot."""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║      AIWork Reference Agent: Customer Support Bot         ║")
    print("║      Intelligent Query Classification & Response          ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    print("📋 Features Demonstrated:")
    print("   • Intent Classification")
    print("   • Knowledge Base Search")
    print("   • Context-Aware Response Generation")
    print("   • Multi-Turn Conversation Support\n")
    print("─" * 60 + "\n")
    
    try:
        # ═══════════════════════════════════════════════════════════
        # Define Support Bot Flow
        # ═══════════════════════════════════════════════════════════
        
        print("🔧 Building customer support pipeline...\n")
        
        flow = Flow("support_bot_v1")
        
        print("   1. ✅ Intent Classification Task")
        flow.add_task(Task("intent", understand_intent))
        
        print("   2. ✅ Knowledge Base Search Task (depends on: intent)")
        flow.add_task(Task("search", search_knowledge_base), depends_on=["intent"])
        
        print("   3. ✅ Response Generation Task (depends on: search)")
        flow.add_task(Task("respond", generate_response), depends_on=["search"])
        
        print("\n   Flow: intent → search → respond\n")
        print("─" * 60 + "\n")

        orchestrator = Orchestrator()
        
        # ═══════════════════════════════════════════════════════════
        # Test Case 1: Refund Request
        # ═══════════════════════════════════════════════════════════
        
        print("💬 Test Case 1: Refund Request\n")
        print("User Query: 'I want a refund for my last order'\n")
        
        ctx1 = {"query": "I want a refund for my last order"}
        
        start_time = time.time()
        res1 = orchestrator.execute(flow, ctx1)
        end_time = time.time()
        
        print("\n" + "─" * 60)
        print("🤖 Bot Response:")
        print("─" * 60)
        response_data = res1['outputs']['respond']
        print(f"\n{response_data['response']}\n")
        print(f"Intent: {response_data['intent']} (confidence: {response_data['confidence']:.0%})")
        print(f"Processing time: {end_time - start_time:.3f}s")
        
        # ═══════════════════════════════════════════════════════════
        # Test Case 2: Hours Inquiry
        # ═══════════════════════════════════════════════════════════
        
        print("\n\n" + "═" * 60 + "\n")
        print("💬 Test Case 2: Hours Inquiry\n")
        print("User Query: 'What are your opening hours?'\n")
        
        ctx2 = {"query": "What are your opening hours?"}
        
        start_time = time.time()
        res2 = orchestrator.execute(flow, ctx2)
        end_time = time.time()
        
        print("\n" + "─" * 60)
        print("🤖 Bot Response:")
        print("─" * 60)
        response_data = res2['outputs']['respond']
        print(f"\n{response_data['response']}\n")
        print(f"Intent: {response_data['intent']} (confidence: {response_data['confidence']:.0%})")
        print(f"Processing time: {end_time - start_time:.3f}s")
        
        # ═══════════════════════════════════════════════════════════
        # Summary
        # ═══════════════════════════════════════════════════════════
        
        print("\n\n" + "═" * 60)
        print("✅ CUSTOMER SUPPORT BOT DEMO COMPLETED")
        print("═" * 60)
        
        print("\n💡 Key Takeaways:")
        print("   • Intent classification routes queries appropriately")
        print("   • Knowledge base provides accurate information")
        print("   • Response generation creates natural language replies")
        print("   • System handles multiple query types efficiently")
        
        print("\n" + "─" * 60)
        print("📚 Next Steps:")
        print("   1. Read: examples/agents/customer_support/README.md")
        print("   2. Customize: Add your own intents and KB articles")
        print("   3. Integrate: Connect to real LLM for better responses")
        print("   4. Enhance: Add conversation history tracking")
        print("─" * 60 + "\n")
        
    except Exception as e:
        print("\n" + "═" * 60)
        print("❌ BOT EXECUTION FAILED")
        print("═" * 60)
        print(f"\nError: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Verify task dependencies are correct")
        print("   2. Check that all handlers return dictionaries")
        print("   3. Ensure query context is provided")
        print("   4. Review examples/agents/customer_support/README.md")
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
