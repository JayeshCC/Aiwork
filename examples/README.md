# 📚 AIWork Examples

Complete guide to all example implementations in the AIWork framework.

---

## Table of Contents

1. [Quick Start Examples](#quick-start-examples)
2. [Reference Agents](#reference-agents)
3. [Running Examples](#running-examples)
4. [Example Outputs](#example-outputs)
5. [Customization Guide](#customization-guide)

---

## Quick Start Examples

### 1. Quickstart (`quickstart.py`)

**What it does:** Simple document processing pipeline demonstrating basic Flow and Task usage.

**Use case:** Learning the fundamentals of AIWork

**Features:**
- Basic task creation
- Simple dependency chain
- Context passing between tasks

**Run:**
```bash
python examples/quickstart.py
```

**Expected Output:**
```
Starting Flow: document_pipeline
  Executing Task: extract...
    [Logic] Extracting text from document...
  Task extract Completed.
  Executing Task: summarize...
  Task summarize Completed.
Flow document_pipeline Finished.

Final Output:
{'extract': {'text': '...'}, 'summarize': {'summary': '...'}}
```

### 2. Memory Demo (`memory_demo.py`)

**What it does:** Demonstrates agent memory and observability features.

**Use case:** Learning context storage and retrieval

**Features:**
- VectorMemory usage
- Agent context recall
- Metrics collection

**Run:**
```bash
python examples/memory_demo.py
```

### 3. Airflow Export Demo (`airflow_export_demo.py`)

**What it does:** Shows how to export AIWork flows to Apache Airflow DAG format.

**Use case:** Integrating with existing Airflow infrastructure

**Features:**
- Flow to DAG conversion
- Airflow-compatible Python code generation

**Run:**
```bash
python examples/airflow_export_demo.py
```

---

## Reference Agents

### 1. Document Processor Agent (`agents/document_processor/run.py`)

**What it does:** Intelligent invoice processing with OCR, analysis, and compliance checking.

**Technologies:**
- OpenVINO-accelerated OCR
- Dynamic task injection (hybrid orchestration)
- Guardrail validation
- Error handling with retries

**Workflow:**
```
Upload Invoice → OCR Extraction → Data Analysis → [Dynamic: Compliance Audit if > $10k] → Store Results
```

**Features:**
- **Hybrid Orchestration:** Dynamically injects compliance audit task for high-value invoices
- **Guardrails:** Validates positive amounts
- **Agent Memory:** Remembers vendor patterns
- **OpenVINO:** 3.7x faster OCR inference (when real OpenVINO is enabled)

**Run:**
```bash
python examples/agents/document_processor/run.py
```

**See detailed guide:** [agents/document_processor/README.md](agents/document_processor/README.md)

### 2. Customer Support Agent (`agents/customer_support/run.py`)

**What it does:** Automated customer support with intent classification, knowledge search, and response generation.

**Technologies:**
- Intent classification
- Knowledge base search
- Multi-turn conversation
- Context-aware responses

**Workflow:**
```
Customer Query → Classify Intent → Search Knowledge Base → Generate Response → Store Interaction
```

**Features:**
- **Intent Classification:** Identifies query type (technical, billing, general)
- **Knowledge Search:** Retrieves relevant information
- **Memory:** Maintains conversation context
- **Escalation:** Routes complex queries to human agents

**Run:**
```bash
python examples/agents/customer_support/run.py
```

**See detailed guide:** [agents/customer_support/README.md](agents/customer_support/README.md)

---

## Running Examples

### Prerequisites

```bash
# Install AIWork
pip install -e .

# Verify installation
python -c "from aiwork import Task, Flow, Orchestrator; print('✅ Ready!')"
```

### Running All Examples

```bash
# Quick start
python examples/quickstart.py

# Memory demo
python examples/memory_demo.py

# Airflow export
python examples/airflow_export_demo.py

# Document processor
python examples/agents/document_processor/run.py

# Customer support
python examples/agents/customer_support/run.py
```

### Expected Execution Time

| Example | Duration | Complexity |
|---------|----------|------------|
| Quickstart | 1-2 seconds | Low |
| Memory Demo | 2-3 seconds | Low |
| Airflow Export | 1 second | Low |
| Document Processor | 3-5 seconds | Medium |
| Customer Support | 3-5 seconds | Medium |

---

## Example Outputs

### Document Processor Output

```
=== Invoice Processing Demo ===

Starting Flow: invoice_processing
  Executing Task: ocr_extract...
    🤖 [Agent: OCR Specialist]
       Goal: Extract text from invoices accurately
       Working on: Extract text and amounts from invoice image
    [Simulated] Performing OCR on invoice...
  Task ocr_extract Completed.
  
  Executing Task: analyze_invoice...
    🤖 [Agent: Financial Analyst]
       Goal: Analyze invoice data for accuracy
       Working on: Analyze extracted invoice data
    [Analysis] Processing invoice data...
    [Analysis] Amount: $12500, Vendor: Intel Corporation
    
    ⚠️ High-value invoice detected ($12500 > $10000)
    🔄 Injecting dynamic compliance audit task...
    
  Task analyze_invoice Completed.
  
  Executing Task: compliance_audit (DYNAMIC)...
    🤖 [Agent: Compliance Officer]
       Goal: Ensure regulatory compliance
       Working on: Audit high-value transaction
    [Compliance] Auditing $12500 payment to Intel Corporation...
    [Compliance] ✅ Compliance check passed
  Task compliance_audit Completed.
  
  Executing Task: store_results...
    [Storage] Saving processed invoice...
  Task store_results Completed.

Flow invoice_processing Finished.

=== Final Results ===
Processed Invoice:
  Amount: $12500
  Vendor: Intel Corporation
  Compliance: APPROVED
  Storage ID: INV-2024-001
```

### Customer Support Output

```
=== Customer Support Bot Demo ===

Starting Flow: support_flow
  Executing Task: classify_intent...
    [Intent] Analyzing query: "My OpenVINO installation failed"
    [Intent] Detected: TECHNICAL_SUPPORT
  Task classify_intent Completed.
  
  Executing Task: search_knowledge...
    [Search] Searching knowledge base for: OpenVINO installation
    [Search] Found 3 relevant articles
  Task search_knowledge Completed.
  
  Executing Task: generate_response...
    [Response] Generating personalized response...
    [Response] Using context from previous interaction
  Task generate_response Completed.

Flow support_flow Finished.

=== Bot Response ===
"I see you're having trouble with OpenVINO installation. Based on your system (Ubuntu 20.04), 
here are the steps:

1. Update your system: sudo apt-get update
2. Install dependencies: sudo apt-get install python3-dev
3. Install OpenVINO: pip install openvino

If the issue persists, please share the error message for further assistance."

Confidence: 92%
Intent: TECHNICAL_SUPPORT
```

---

## Customization Guide

### Adapting Document Processor for Your Use Case

**Example: Processing Contracts Instead of Invoices**

```python
# 1. Update the agent's role and goal
ocr_agent = Agent(
    role="Contract Specialist",  # Changed from "OCR Specialist"
    goal="Extract clauses and parties from contracts",  # Changed goal
    backstory="Expert in legal document analysis"
)

# 2. Modify the OCR handler
def ocr_contract(ctx):
    contract = ctx["contract_path"]
    # Your OCR logic here
    return {
        "parties": ["Company A", "Company B"],
        "clauses": ["Term: 2 years", "Payment: Monthly"],
        "date": "2024-01-01"
    }

# 3. Update analysis logic
def analyze_contract(ctx):
    data = ctx["outputs"]["ocr_contract"]
    # Your analysis logic
    return {
        "risk_level": "low",
        "requires_review": data.get("value", 0) > 100000
    }
```

### Adding New Tasks to Existing Flows

```python
# Add email notification task
def send_notification(ctx):
    result = ctx["outputs"]["final_task"]
    # Send email with result
    return {"email_sent": True, "recipient": "admin@example.com"}

flow.add_task(
    Task("notify", send_notification),
    depends_on=["final_task"]
)
```

### Customizing Agent Behavior

```python
# Add custom tools
def custom_validation_tool(data):
    # Your validation logic
    return {"valid": True, "confidence": 0.95}

agent = Agent(
    role="Custom Validator",
    goal="Validate data according to business rules",
    tools=[custom_validation_tool],  # Add your tools
    memory=VectorMemory(),  # Optional memory
    verbose=True  # Show thinking process
)
```

---

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'aiwork'`

**Solution:**
```bash
# Make sure you've installed the package
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

**Issue:** Examples run but produce no output

**Solution:**
- Check that all task handlers return dictionaries
- Ensure dependencies are correct in flow.add_task()
- Run with verbose=True on agents to see thinking process

**Issue:** Memory not working

**Solution:**
```python
# Make sure memory is attached to agent
memory = VectorMemory()
memory.add("context information")

agent = Agent(
    role="...",
    memory=memory  # Don't forget this!
)
```

---

## Next Steps

1. **Start with quickstart.py** to understand basics
2. **Run memory_demo.py** to see context management
3. **Explore document_processor** for real-world workflow
4. **Study customer_support** for multi-turn interactions
5. **Customize examples** for your specific use case

---

## Additional Resources

- [User Guide](../docs/USER_GUIDE.md) - Comprehensive tutorial
- [Architecture](../docs/ARCHITECTURE.md) - System design
- [API Reference](../docs/API_REFERENCE.md) - Complete API docs
- [Deployment Guide](../docs/DEPLOYMENT.md) - Production deployment

---

**Happy Building! 🚀**

For questions or issues, please open an issue on GitHub or check the FAQ in the User Guide.
