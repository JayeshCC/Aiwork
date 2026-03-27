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


def progress(steps, tone=GREEN, delay=0.05):
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
    
    section("  Stage 1: Intent Classification", CYAN)
    print(color(f"    Customer query received: '{query}'", WHITE))
    progress(
        [
            "Normalizing input",
            "Scanning for key phrases",
            "Scoring likely intents",
        ],
        tone=CYAN,
    )
    
    # Simple keyword-based classification (replace with ML model)
    query_lower = query.lower()
    
    if "refund" in query_lower or "money back" in query_lower:
        intent = "refund_request"
        confidence = 0.95
        print(color(f"    Detected intent: REFUND_REQUEST ({confidence:.0%})", GREEN))
    elif "hours" in query_lower or "open" in query_lower or "schedule" in query_lower:
        intent = "check_hours"
        confidence = 0.98
        print(color(f"    Detected intent: CHECK_HOURS ({confidence:.0%})", GREEN))
    else:
        intent = "general_inquiry"
        confidence = 0.80
        print(color(f"    Detected intent: GENERAL_INQUIRY ({confidence:.0%})", GREEN))
    
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
    
    section("  Stage 2: Knowledge Retrieval", BLUE)
    print(color(f"    Searching support knowledge base for: {intent}", WHITE))
    progress(
        [
            "Embedding intent",
            "Running similarity match",
            "Selecting top article",
        ],
        tone=BLUE,
    )
    
    # Simulated knowledge base (replace with real vector DB)
    kb = {
        "refund_request": "Refunds are processed within 3-5 business days. Please provide your order number and reason for the refund request.",
        "check_hours": "We are open Monday-Friday, 9am-5pm EST. Weekend hours: Saturday 10am-3pm. Closed on Sundays and major holidays.",
        "general_inquiry": "For general inquiries, please contact support@example.com or call 1-800-SUPPORT. Our team typically responds within 24 hours."
    }
    
    result = kb.get(intent, "No relevant information found.")
    
    print(color(f"    Retrieved support article ({len(result)} chars)", GREEN))
    
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
    
    section("  Stage 3: Response Generation", MAGENTA)
    progress(
        [
            "Combining query and support article",
            "Drafting reply",
            "Preparing follow-up suggestions",
        ],
        tone=MAGENTA,
    )
    
    # Simple template-based response (replace with LLM)
    response = f"Here is the information you requested: {kb_result}"
    
    print(color(f"    Response drafted ({len(response)} chars)", GREEN))
    
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
    
    print(color("╔═══════════════════════════════════════════════════════════╗", BOLD + CYAN))
    print(color("║      AIWork Reference Agent: Customer Support Bot         ║", BOLD + CYAN))
    print(color("║      Intelligent Query Classification & Response          ║", BOLD + CYAN))
    print(color("╚═══════════════════════════════════════════════════════════╝\n", BOLD + CYAN))

    print(color("Features Demonstrated:", BOLD + WHITE))
    print(color("   • Intent Classification", WHITE))
    print(color("   • Knowledge Base Search", WHITE))
    print(color("   • Context-Aware Response Generation", WHITE))
    print(color("   • Multi-Turn Conversation Support\n", WHITE))
    print("─" * 60 + "\n")
    
    try:
        # ═══════════════════════════════════════════════════════════
        # Define Support Bot Flow
        # ═══════════════════════════════════════════════════════════
        
        section("Building customer support pipeline...", CYAN)
        progress(
            [
                "Registering intent stage",
                "Registering search stage",
                "Registering response stage",
                "Compiling support flow",
            ],
            tone=GREEN,
        )
        print()
        
        flow = Flow("support_bot_v1")
        
        print(color("   1. Intent Classification Task ready", GREEN))
        flow.add_task(Task("intent", understand_intent))
        
        print(color("   2. Knowledge Base Search Task ready    depends on: intent", GREEN))
        flow.add_task(Task("search", search_knowledge_base), depends_on=["intent"])
        
        print(color("   3. Response Generation Task ready      depends on: search", GREEN))
        flow.add_task(Task("respond", generate_response), depends_on=["search"])
        
        print(color("\n   Flow: intent -> search -> respond\n", DIM + WHITE))
        print("─" * 60 + "\n")

        orchestrator = Orchestrator()
        
        # ═══════════════════════════════════════════════════════════
        # Test Case 1: Refund Request
        # ═══════════════════════════════════════════════════════════
        
        section("Test Case 1: Refund Request", YELLOW)
        print(color("User Query: 'I want a refund for my last order'\n", WHITE))
        
        ctx1 = {"query": "I want a refund for my last order"}
        
        start_time = time.time()
        res1 = orchestrator.execute(flow, ctx1)
        end_time = time.time()
        
        print("\n" + "─" * 60)
        print(color("Bot Response:", BOLD + GREEN))
        print("─" * 60)
        response_data = res1['outputs']['respond']
        print(color(f"\n{response_data['response']}\n", WHITE))
        print(color(f"Intent: {response_data['intent']} (confidence: {response_data['confidence']:.0%})", WHITE))
        print(color(f"Processing time: {end_time - start_time:.3f}s", WHITE))
        
        # ═══════════════════════════════════════════════════════════
        # Test Case 2: Hours Inquiry
        # ═══════════════════════════════════════════════════════════
        
        print("\n\n" + "═" * 60 + "\n")
        section("Test Case 2: Hours Inquiry", YELLOW)
        print(color("User Query: 'What are your opening hours?'\n", WHITE))
        
        ctx2 = {"query": "What are your opening hours?"}
        
        start_time = time.time()
        res2 = orchestrator.execute(flow, ctx2)
        end_time = time.time()
        
        print("\n" + "─" * 60)
        print(color("Bot Response:", BOLD + GREEN))
        print("─" * 60)
        response_data = res2['outputs']['respond']
        print(color(f"\n{response_data['response']}\n", WHITE))
        print(color(f"Intent: {response_data['intent']} (confidence: {response_data['confidence']:.0%})", WHITE))
        print(color(f"Processing time: {end_time - start_time:.3f}s", WHITE))
        
        # ═══════════════════════════════════════════════════════════
        # Summary
        # ═══════════════════════════════════════════════════════════
        
        print("\n\n" + "═" * 60)
        print(color("CUSTOMER SUPPORT BOT DEMO COMPLETED", BOLD + GREEN))
        print("═" * 60)
        
        print(color("\nKey Takeaways:", BOLD + WHITE))
        print(color("   • Intent classification routes queries appropriately", WHITE))
        print(color("   • Knowledge base provides accurate information", WHITE))
        print(color("   • Response generation creates natural language replies", WHITE))
        print(color("   • System handles multiple query types efficiently", WHITE))
        
        print("\n" + "─" * 60)
        print(color("Next Steps:", BOLD + WHITE))
        print(color("   1. Read: examples/agents/customer_support/README.md", WHITE))
        print(color("   2. Customize: Add your own intents and KB articles", WHITE))
        print(color("   3. Integrate: Connect to real LLM for better responses", WHITE))
        print(color("   4. Enhance: Add conversation history tracking", WHITE))
        print("─" * 60 + "\n")
        
    except Exception as e:
        print("\n" + "═" * 60)
        print(color("BOT EXECUTION FAILED", BOLD + RED))
        print("═" * 60)
        print(color(f"\nError: {str(e)}", RED))
        print(color("\nTroubleshooting Tips:", BOLD + WHITE))
        print(color("   1. Verify task dependencies are correct", WHITE))
        print(color("   2. Check that all handlers return dictionaries", WHITE))
        print(color("   3. Ensure query context is provided", WHITE))
        print(color("   4. Review examples/agents/customer_support/README.md", WHITE))
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
