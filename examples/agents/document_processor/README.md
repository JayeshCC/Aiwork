# 📄 Document Processor Agent

Intelligent document processing pipeline with OCR, analysis, and dynamic compliance checking.

---

## Overview

This reference agent demonstrates a real-world use case: processing financial invoices with automated compliance auditing for high-value transactions.

**Key Innovation:** Uses **hybrid orchestration** to dynamically inject compliance audit tasks based on invoice amount.

---

## Features

### 1. OpenVINO-Accelerated OCR
- Extracts text from invoice images
- Uses Intel OpenVINO for 3.7x faster inference (when enabled)
- Handles multiple image formats

### 2. Intelligent Analysis
- Parses invoice data (amount, vendor, date)
- Calculates risk scores
- Validates data completeness

### 3. Dynamic Compliance Checking
- **Hybrid Orchestration:** Automatically injects audit task for invoices > $1,000
- Demonstrates agent-driven workflow modification
- No complex branching logic needed

### 4. Guardrail Validation
- Ensures positive amounts
- Validates data format
- Prevents invalid data propagation

### 5. Error Handling
- Automatic retries on transient failures
- Graceful degradation
- Detailed error logging

---

## Workflow

```
┌─────────────────┐
│  Upload Invoice │
└────────┬────────┘
         ↓
┌─────────────────┐
│  OCR Extraction │  ← OpenVINO accelerated
└────────┬────────┘
         ↓
┌─────────────────┐
│  Data Analysis  │
└────────┬────────┘
         ↓
    ╔═══════════════════════╗
    ║ Amount > $1,000?      ║
    ╚═══════════════════════╝
         ↓ Yes          ↓ No
┌──────────────────┐    │
│ Compliance Audit │ ←──┘
│   (DYNAMIC)      │
└────────┬─────────┘
         ↓
┌─────────────────┐
│  Store Results  │
└─────────────────┘
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
python examples/agents/document_processor/run.py
```

### Expected Output

```
=== Invoice Processing Demo ===

Starting Flow: invoice_processing
  Executing Task: ocr_extract...
    🤖 [Agent: OCR Specialist]
       Goal: Extract text from invoices accurately
    [Simulated] Performing OCR on invoice...
  Task ocr_extract Completed.
  
  Executing Task: analyze_invoice...
    🤖 [Agent: Financial Analyst]
    [Analysis] Amount: $5000, Vendor: Intel Corporation
    
    ⚠️ High-value invoice detected!
    🔄 Injecting dynamic compliance audit task...
    
  Task analyze_invoice Completed.
  
  Executing Task: compliance_audit (DYNAMIC)...
    🤖 [Agent: Compliance Officer]
    [Compliance] ✅ Compliance check passed
  Task compliance_audit Completed.

=== Final Results ===
Processed Invoice:
  Amount: $5000
  Vendor: Intel Corporation
  Compliance: APPROVED
```

---

## Code Walkthrough

### 1. Agent Definitions

```python
# OCR Agent - Specialized in text extraction
ocr_agent = Agent(
    role="OCR Specialist",
    goal="Extract text from invoices accurately",
    backstory="Expert in document digitization with 99% accuracy"
)

# Financial Agent - Analyzes invoice data
analyst_agent = Agent(
    role="Financial Analyst",
    goal="Analyze invoice data for accuracy and compliance",
    backstory="20 years experience in financial document review"
)

# Compliance Agent - Audits high-value transactions
compliance_agent = Agent(
    role="Compliance Officer",
    goal="Ensure regulatory compliance for financial transactions",
    backstory="Certified compliance specialist"
)
```

### 2. Dynamic Task Injection (Hybrid Orchestration)

```python
def analyze_invoice(ctx):
    invoice_data = ctx["outputs"]["ocr_extract"]["data"]
    amount = invoice_data["amount"]
    
    result = {
        "amount": amount,
        "vendor": invoice_data["vendor"],
        "risk_score": calculate_risk(amount)
    }
    
    # KEY FEATURE: Dynamic task injection
    if amount > 1000:
        print("⚠️ High-value invoice detected!")
        print("🔄 Injecting dynamic compliance audit task...")
        
        # Create audit task
        audit_task = Task(
            name="compliance_audit",
            description=f"Audit ${amount} payment",
            agent=compliance_agent,
            handler=compliance_audit_handler
        )
        
        # This task will be executed next!
        result["next_tasks"] = [audit_task]
    
    return result
```

### 3. Guardrail Validation

```python
# Define validation rule
def validate_positive_amount(output):
    return output.get("amount", 0) > 0

# Create guardrail
amount_guardrail = Guardrail(
    name="positive_amount",
    validator=validate_positive_amount,
    description="Ensures invoice amount is positive"
)

# Apply to task
analyze_task = Task(
    "analyze",
    analyze_handler,
    guardrails=[amount_guardrail]  # Validation enforced
)
```

---

## Customization Guide

### Processing Different Document Types

**Example: Processing Purchase Orders**

```python
# 1. Update agent roles
ocr_agent = Agent(
    role="PO Specialist",
    goal="Extract line items from purchase orders",
    backstory="Expert in procurement documents"
)

# 2. Modify OCR handler
def ocr_purchase_order(ctx):
    # Your OCR logic for POs
    return {
        "po_number": "PO-2024-001",
        "line_items": [
            {"item": "Laptop", "qty": 10, "price": 1200},
            {"item": "Monitor", "qty": 20, "price": 300}
        ],
        "total": 18000
    }

# 3. Update analysis
def analyze_po(ctx):
    po_data = ctx["outputs"]["ocr_po"]
    # Your PO analysis logic
    return {"approved": True, "approval_level": "manager"}
```

### Changing Compliance Threshold

```python
# Change from $1,000 to $5,000
COMPLIANCE_THRESHOLD = 5000

def analyze_invoice(ctx):
    amount = ctx["outputs"]["ocr"]["amount"]
    
    if amount > COMPLIANCE_THRESHOLD:  # Changed threshold
        # Inject audit task
        ...
```

### Adding Email Notifications

```python
def send_notification(ctx):
    """Send email with processing results"""
    result = ctx["outputs"]["store"]
    
    # Your email logic
    send_email(
        to="finance@company.com",
        subject=f"Invoice {result['id']} Processed",
        body=f"Amount: ${result['amount']}, Status: {result['status']}"
    )
    
    return {"notification_sent": True}

# Add to flow
flow.add_task(
    Task("notify", send_notification),
    depends_on=["store"]
)
```

---

## Performance Optimization

### With Real OpenVINO

```python
# Install OpenVINO
# pip install openvino

from aiwork.integrations.openvino_adapter import OpenVINOAdapter

# Load optimized model
ov_ocr = OpenVINOAdapter("models/ocr_model.xml")

def ocr_handler_optimized(ctx):
    image = ctx["image"]
    result = ov_ocr.infer({"image": image})  # 3.7x faster!
    return {"text": result["text"]}
```

**Performance Comparison:**
- Baseline (PyTorch/ONNX): 156ms per image
- With OpenVINO: 42ms per image
- **Speedup: 3.7x** ✅

---

## Troubleshooting

### Issue: Dynamic task not executing

**Cause:** Task injection syntax incorrect

**Solution:**
```python
# Correct way
result = {...}
result["next_tasks"] = [task1, task2]  # List of Task objects
return result

# Incorrect
result["next_tasks"] = task1  # Must be a list!
```

### Issue: Guardrail always failing

**Cause:** Validation function returning None instead of boolean

**Solution:**
```python
# Correct
def validator(output):
    return output.get("amount", 0) > 0  # Returns True/False

# Incorrect
def validator(output):
    if output.get("amount", 0) > 0:
        pass  # Returns None!
```

---

## Related Examples

- **Customer Support Agent:** Multi-turn conversation handling
- **Memory Demo:** Context storage and retrieval
- **Airflow Export:** Converting flows to Airflow DAGs

---

## Additional Resources

- [User Guide](../../../docs/USER_GUIDE.md) - Comprehensive tutorial
- [Architecture](../../../docs/ARCHITECTURE.md) - System design
- [API Reference](../../../docs/API_REFERENCE.md) - API documentation
- [Benchmarks](../../../docs/BENCHMARKS.md) - Performance data

---

**Built with ❤️ for the Intel AI Innovation Challenge 2024**
