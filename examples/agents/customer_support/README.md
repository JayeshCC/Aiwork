# 🎧 Customer Support Agent

Automated customer support bot with intent classification, knowledge search, and response generation.

---

## Overview

This reference agent demonstrates an intelligent customer support system that handles multiple query types through a three-stage pipeline: intent classification, knowledge base search, and response generation.

**Key Innovation:** Uses **context-aware processing** to understand customer intent and provide relevant, personalized responses.

---

## Features

### 1. Intent Classification
- Analyzes customer queries to identify intent
- Supports multiple intent categories
- Returns confidence scores
- Handles ambiguous queries

### 2. Knowledge Base Search
- Retrieves relevant information based on intent
- Fast vector-based search
- Ranks results by relevance
- Handles missing information gracefully

### 3. Response Generation
- Creates natural language responses
- Combines KB information with query context
- Personalizes based on conversation history
- Includes follow-up suggestions

### 4. Multi-Turn Conversation
- Maintains context across interactions
- Tracks conversation history
- Handles clarification questions
- Escalates to human agents when needed

---

## Workflow

```
┌────────────────┐
│ Customer Query │
└───────┬────────┘
        ↓
┌────────────────────┐
│ Intent             │  ← Classify query type
│ Classification     │     (refund, hours, technical, etc.)
└───────┬────────────┘
        ↓
┌────────────────────┐
│ Knowledge Base     │  ← Search for relevant info
│ Search             │     using vector similarity
└───────┬────────────┘
        ↓
┌────────────────────┐
│ Response           │  ← Generate natural language
│ Generation         │     response with context
└───────┬────────────┘
        ↓
┌────────────────────┐
│ Customer Response  │
└────────────────────┘
```

---

## Running the Example

### Prerequisites

```bash
# Install AIWork
pip install -e .

# Verify installation
python -c "from aiwork import Task, Flow; print('✅ Ready!')"
```

### Basic Execution

```bash
python examples/agents/customer_support/run.py
```

### Expected Output

```
=== Customer Support Bot Demo ===

💬 Test Case 1: Refund Request

User Query: 'I want a refund for my last order'

Starting Flow: support_bot_v1
  Executing Task: intent...
    [Intent] Analyzing query: 'I want a refund for my last order'
    [Intent] ✅ Detected: REFUND_REQUEST (confidence: 0.95)
  Task intent Completed.
  
  Executing Task: search...
    [Search] Searching knowledge base for: refund_request
    [Search] ✅ Found relevant information
  Task search Completed.
  
  Executing Task: respond...
    [Response] Generating personalized response...
    [Response] ✅ Generated response
  Task respond Completed.

🤖 Bot Response:
────────────────────────────────────────────────────────────

Here is the information you requested: Refunds are processed within 
3-5 business days. Please provide your order number and reason for 
the refund request.

Intent: refund_request (confidence: 95%)
Processing time: 0.003s
```

---

## Code Walkthrough

### 1. Intent Classification

```python
def understand_intent(ctx):
    """
    Classify customer query intent.
    
    In production, use ML models like BERT or transformers.
    """
    query = ctx.get("query", "")
    
    # Keyword-based classification (replace with ML model)
    if "refund" in query.lower():
        return {
            "intent": "refund_request",
            "confidence": 0.95
        }
    elif "hours" in query.lower():
        return {
            "intent": "check_hours",
            "confidence": 0.98
        }
    
    return {
        "intent": "general_inquiry",
        "confidence": 0.80
    }
```

### 2. Knowledge Base Search

```python
def search_knowledge_base(ctx):
    """
    Search KB for relevant information.
    
    In production, use vector search (FAISS, Pinecone).
    """
    intent = ctx["outputs"]["intent"]["intent"]
    
    # Simulated KB (replace with vector database)
    kb = {
        "refund_request": "Refunds are processed within 3-5 business days...",
        "check_hours": "We are open Mon-Fri, 9am-5pm EST...",
        "general_inquiry": "Please contact support@example.com..."
    }
    
    return {
        "kb_result": kb.get(intent, "No info found."),
        "relevance_score": 0.92
    }
```

### 3. Response Generation

```python
def generate_response(ctx):
    """
    Generate natural language response.
    
    In production, use LLMs (GPT-4, Claude).
    """
    kb_result = ctx["outputs"]["search"]["kb_result"]
    
    # Template-based response (replace with LLM)
    response = f"Here is the information you requested: {kb_result}"
    
    return {
        "response": response,
        "follow_up_suggestions": [
            "Is there anything else I can help you with?",
            "Would you like to speak with a human agent?"
        ]
    }
```

### 4. Building the Flow

```python
flow = Flow("support_bot_v1")

# Step 1: Classify intent
flow.add_task(Task("intent", understand_intent))

# Step 2: Search knowledge base (depends on intent)
flow.add_task(Task("search", search_knowledge_base), depends_on=["intent"])

# Step 3: Generate response (depends on search)
flow.add_task(Task("respond", generate_response), depends_on=["search"])

# Execute
orchestrator = Orchestrator()
result = orchestrator.execute(flow, {"query": "I want a refund"})
```

---

## Customization Guide

### Adding New Intents

```python
def understand_intent(ctx):
    query = ctx.get("query", "").lower()
    
    # Add new intents
    if "track" in query or "order status" in query:
        return {"intent": "order_tracking", "confidence": 0.93}
    elif "password" in query or "login" in query:
        return {"intent": "account_access", "confidence": 0.91}
    
    # Existing intents...
```

### Expanding Knowledge Base

```python
def search_knowledge_base(ctx):
    intent = ctx["outputs"]["intent"]["intent"]
    
    kb = {
        "refund_request": "Refunds are processed within 3-5 business days...",
        "check_hours": "We are open Mon-Fri, 9am-5pm EST...",
        "order_tracking": "To track your order, visit our tracking page...",
        "account_access": "Password reset links expire after 24 hours...",
        # Add more KB articles
    }
    
    return {"kb_result": kb.get(intent, "No info found.")}
```

### Integrating with Real LLM

```python
import openai  # or anthropic for Claude

def generate_response(ctx):
    kb_result = ctx["outputs"]["search"]["kb_result"]
    query = ctx["outputs"]["intent"]["original_query"]
    
    # Use GPT-4 for response generation
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful customer support agent."},
            {"role": "user", "content": f"Query: {query}\n\nKB Info: {kb_result}\n\nRespond naturally:"}
        ]
    )
    
    return {
        "response": response.choices[0].message.content,
        "model": "gpt-4"
    }
```

### Adding Conversation History

```python
# Store conversation history
conversation_history = []

def generate_response(ctx):
    kb_result = ctx["outputs"]["search"]["kb_result"]
    current_query = ctx.get("query", "")
    
    # Add to history
    conversation_history.append({
        "query": current_query,
        "response": kb_result
    })
    
    # Use history for context
    context = f"Previous conversation: {conversation_history[-3:]}"  # Last 3 turns
    
    return {
        "response": f"{context}\n\nCurrent response: {kb_result}",
        "history_length": len(conversation_history)
    }
```

---

## Advanced Features

### Agent Escalation

```python
def generate_response(ctx):
    confidence = ctx["outputs"]["intent"]["confidence"]
    kb_result = ctx["outputs"]["search"]["kb_result"]
    
    # Escalate to human if low confidence
    if confidence < 0.70:
        return {
            "response": "I'm not sure I understand. Let me connect you with a human agent.",
            "escalated": True,
            "reason": "low_confidence"
        }
    
    return {"response": kb_result, "escalated": False}
```

### Sentiment Analysis

```python
def understand_intent(ctx):
    query = ctx.get("query", "")
    
    # Detect sentiment
    negative_words = ["angry", "frustrated", "terrible", "worst"]
    sentiment = "negative" if any(word in query.lower() for word in negative_words) else "neutral"
    
    # Classify intent...
    
    return {
        "intent": intent,
        "confidence": confidence,
        "sentiment": sentiment  # Added sentiment
    }
```

### Multi-Language Support

```python
from langdetect import detect

def understand_intent(ctx):
    query = ctx.get("query", "")
    
    # Detect language
    language = detect(query)
    
    # Translate to English if needed
    if language != "en":
        query = translate_to_english(query)
    
    # Classify intent...
    
    return {
        "intent": intent,
        "confidence": confidence,
        "language": language
    }
```

---

## Performance Optimization

### Caching KB Results

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def search_knowledge_base_cached(intent):
    # Your KB search logic
    return kb_result

def search_knowledge_base(ctx):
    intent = ctx["outputs"]["intent"]["intent"]
    result = search_knowledge_base_cached(intent)
    return {"kb_result": result}
```

### Async Processing

```python
import asyncio

async def understand_intent_async(ctx):
    # Async intent classification
    result = await classify_async(ctx.get("query"))
    return result

# Use with async orchestrator
```

---

## Troubleshooting

### Issue: Intent classification always returns general_inquiry

**Cause:** Keywords not matched

**Solution:**
```python
# Add more keywords or use ML model
if any(word in query.lower() for word in ["refund", "return", "money back"]):
    return {"intent": "refund_request", "confidence": 0.95}
```

### Issue: KB search returns "No info found"

**Cause:** Intent not in KB dictionary

**Solution:**
```python
# Add default fallback
kb_result = kb.get(intent, "I don't have specific information about that. Let me connect you with a specialist.")
```

### Issue: Response too generic

**Cause:** Not using query context

**Solution:**
```python
# Include original query in response
def generate_response(ctx):
    query = ctx["outputs"]["intent"]["original_query"]
    kb_result = ctx["outputs"]["search"]["kb_result"]
    
    response = f"Regarding your question about '{query}': {kb_result}"
    return {"response": response}
```

---

## Testing

### Unit Testing

```python
def test_intent_classification():
    result = understand_intent({"query": "I want a refund"})
    assert result["intent"] == "refund_request"
    assert result["confidence"] > 0.9

def test_kb_search():
    ctx = {"outputs": {"intent": {"intent": "check_hours"}}}
    result = search_knowledge_base(ctx)
    assert "open" in result["kb_result"].lower()
```

### Integration Testing

```python
def test_full_flow():
    flow = Flow("support_bot_test")
    flow.add_task(Task("intent", understand_intent))
    flow.add_task(Task("search", search_knowledge_base), depends_on=["intent"])
    flow.add_task(Task("respond", generate_response), depends_on=["search"])
    
    orchestrator = Orchestrator()
    result = orchestrator.execute(flow, {"query": "What are your hours?"})
    
    assert "response" in result["outputs"]["respond"]
    assert result["outputs"]["intent"]["intent"] == "check_hours"
```

---

## Related Examples

- **Document Processor:** Hybrid orchestration with dynamic tasks
- **Memory Demo:** Agent memory and context management
- **Quickstart:** Basic flow and task patterns

---

## Additional Resources

- [User Guide](../../../docs/USER_GUIDE.md) - Comprehensive tutorial
- [Architecture](../../../docs/ARCHITECTURE.md) - System design
- [API Reference](../../../docs/API_REFERENCE.md) - API documentation
- [Examples Guide](../../README.md) - All examples overview

---

## Metrics and Monitoring

```python
from aiwork.core.observability import metrics

# Track response time
start = time.time()
result = orchestrator.execute(flow, ctx)
duration = time.time() - start

metrics.record("response_time", duration, tags={"intent": result["intent"]})

# Track intent distribution
metrics.increment("intent_count", tags={"intent": intent})

# Track escalations
if result["escalated"]:
    metrics.increment("escalations", tags={"reason": result["reason"]})
```

---

**Built with ❤️ for the Intel AI Innovation Challenge 2024**
