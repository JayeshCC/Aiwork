# Document Processor Agent - Usage Guide

## Running the Example

### Correct Command

```bash
# From repository root
python examples/agents/document_processor/run.py

# Or using python3
python3 examples/agents/document_processor/run.py

# Or as module (if package installed)
python -m examples.agents.document_processor.run
```

### Prerequisites

The example requires the AIWork package to be installed. Install it in development mode:

```bash
# From repository root
pip install -e .
```

## Common Errors

### File Not Found Error

**Problem:**
```bash
python3 examples/agents/document_processor/run. py
# Error: [Errno 2] No such file or directory: 'examples/agents/document_processor/run. py'
```

**Cause:** Typo with space before extension: `run. py` instead of `run.py`

**Solution:** Remove the space:
```bash
python examples/agents/document_processor/run.py
```

### Import Error

**Problem:**
```bash
ModuleNotFoundError: No module named 'aiwork'
```

**Solution:** Install package first:
```bash
pip install -e .
python examples/agents/document_processor/run.py
```

### Wrong Directory Error

**Problem:**
```bash
python run.py
# Error: ModuleNotFoundError or FileNotFoundError
```

**Solution:** Run from repository root, not from the example directory:
```bash
# Wrong - from inside examples/agents/document_processor/
cd examples/agents/document_processor
python run.py

# Correct - from repository root
cd /path/to/Aiwork
python examples/agents/document_processor/run.py
```

### OpenVINO Warning

**Problem:**
```
Initialized OpenVINO Adapter for model: models/ocr_model.xml
⚠️  OpenVINO model not found, using simulated OCR
```

**Solution:** This is expected behavior. The example uses a simulated OpenVINO adapter for demonstration. To use real OpenVINO:

1. Install OpenVINO: `pip install openvino`
2. Download a real OCR model
3. Update model path in code
4. See `docs/ARCHITECTURE.md` for full setup

## Expected Output

When you run the example successfully, you should see:

```
╔═══════════════════════════════════════════════════════════╗
║      AIWork Reference Agent: Document Processor           ║
║      Intelligent Invoice Processing Pipeline              ║
╚═══════════════════════════════════════════════════════════╝

📋 Features Demonstrated:
   • Agent-Centric Architecture
   • Hybrid Orchestration (Dynamic Task Injection)
   • OpenVINO Hardware Acceleration
   • Guardrail Validation
   • Multi-Agent Collaboration

────────────────────────────────────────────────────────────

🔧 Building invoice processing pipeline...

   1. ✅ OCR Task (Agent: Document Processor)
   2. ✅ Analysis Task (Agent: Financial Analyst)
      • Includes dynamic compliance task injection logic

────────────────────────────────────────────────────────────

▶️  Executing pipeline...

Starting Flow: finance_pipeline
  Executing Task: ocr_task...
    > Assigned to Agent: Document Processor
    [OCR] Processing document: uploads/invoice_nov.pdf
    [OCR] Using OpenVINO acceleration for fast inference...
    [OCR] ✅ Successfully extracted 66 characters
  Task ocr_task Completed.
  
  Executing Task: analyze_task...
    > Assigned to Agent: Financial Analyst
    [Analysis] Parsing invoice data...
    [Analysis] Amount: $5000.00
    [Analysis] Vendor: Intel Corp
    
    ⚠️  High-value transaction detected ($5000.00 > $1000)
    🔄 Triggering dynamic compliance audit...
    ✅ Compliance audit task scheduled
    
  Task analyze_task Completed.
    [Dynamic] Agent requested 1 new tasks.
    
  Executing Task: audit_task...
    > Assigned to Agent: Compliance Officer
  Task audit_task Completed.
  
Flow finance_pipeline Finished.

════════════════════════════════════════════════════════════
✅ PIPELINE COMPLETED SUCCESSFULLY
════════════════════════════════════════════════════════════

⏱️  Total Execution Time: 0.0003s

📊 Task Outputs:

   ocr_task:
      • raw_text: Invoice #12345...
      
   analyze_task:
      • analysis: Invoice data extracted successfully
      • amount: 5000.0
      • vendor: Intel Corp
      • risk_score: 0.15
      
   audit_task:
      • audit_status: APPROVED
      • reason: Vendor is trusted
      • auditor: Compliance Officer
      • timestamp: 1234567890.123

────────────────────────────────────────────────────────────
💡 Key Takeaways:
   • Hybrid orchestration enables adaptive workflows
   • Agents collaborate to process complex documents
   • Guardrails ensure data quality at each step
   • OpenVINO provides hardware acceleration
```

## Customization

### Using Real Invoice Data

Replace simulated data with real invoice processing:

```python
# In ocr_extract handler:
def ocr_extract(ctx):
    invoice_path = ctx.get("input_path", "invoice.pdf")
    
    # Use real OCR library (pytesseract, OpenVINO, etc.)
    from PIL import Image
    import pytesseract
    
    image = Image.open(invoice_path)
    text = pytesseract.image_to_string(image)
    
    return {"raw_text": text}
```

### Modifying Compliance Threshold

Change the dollar amount that triggers compliance audit:

```python
# In analyze_finance handler:
if amount > 1000:  # Change this threshold
    # Inject compliance task
    print(f"\n    ⚠️  High-value transaction detected (${amount:.2f} > $1000)")
```

For example, to only audit transactions over $10,000:

```python
if amount > 10000:  # New threshold
    # Inject compliance task
```

### Adding New Agents

Add additional processing steps to the pipeline:

```python
# Define a new agent
quality_agent = Agent(
    role="Quality Assurance",
    goal="Verify data accuracy",
    backstory="Meticulous QA specialist with attention to detail"
)

# Create handler
def quality_check(ctx):
    """Validate extracted data quality."""
    text = ctx["outputs"]["ocr_task"]["raw_text"]
    
    # Add validation logic
    has_amount = "$" in text
    has_date = any(year in text for year in ["2023", "2024", "2025"])
    
    return {
        "quality_score": 0.95 if has_amount and has_date else 0.5,
        "validation": "PASSED" if has_amount and has_date else "FAILED"
    }

# Add to flow
quality_task = Task(
    name="quality_task",
    description="Validate data quality",
    agent=quality_agent,
    handler=quality_check
)

flow.add_task(quality_task, depends_on=["ocr_task"])
```

### Modifying Guardrails

Create custom validation rules:

```python
# Create a stricter amount validation
def validate_realistic_amount(data):
    """Ensure amounts are within realistic bounds."""
    text = data.get("raw_text", "")
    
    # Extract amount (simplified)
    import re
    amounts = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
    
    if not amounts:
        return False
    
    # Check if amount is reasonable (not too high)
    amount_str = amounts[0].replace('$', '').replace(',', '')
    amount = float(amount_str)
    
    return 0 < amount < 1000000  # Between $0 and $1M

# Use in task
amount_guardrail = Guardrail(
    name="realistic_amount_check",
    validator=validate_realistic_amount,
    description="Ensures extracted amounts are within realistic bounds"
)

task = Task(
    name="ocr_task",
    handler=ocr_extract,
    guardrails=[amount_guardrail]
)
```

## Architecture Overview

The document processor demonstrates key AIWork features:

### 1. Multi-Agent Collaboration

Three specialized agents work together:
- **Document Processor**: OCR extraction using OpenVINO
- **Financial Analyst**: Invoice analysis and risk assessment
- **Compliance Officer**: Regulatory audit for high-value transactions

### 2. Hybrid Orchestration

The workflow combines:
- **Static DAG**: Pre-defined OCR → Analysis pipeline
- **Dynamic Injection**: Compliance task added at runtime based on amount

### 3. Guardrails

Data validation ensures quality:
```python
amount_guardrail = Guardrail(
    name="positive_amount_check",
    validator=validate_positive_amount,
    description="Ensures the output contains a currency symbol"
)
```

### 4. Tool Integration

Agents use tools for specialized capabilities:
```python
ocr_agent = Agent(
    role="Document Processor",
    tools=[ov_adapter]  # OpenVINO for hardware acceleration
)
```

## Testing

The example is covered by automated tests in `tests/test_examples.py`:

```bash
# Run all example tests
pytest tests/test_examples.py -v

# Run only document processor test
pytest tests/test_examples.py::test_document_processor_logic -v
```

## Troubleshooting

### Example Doesn't Execute

1. **Check you're in the right directory:**
   ```bash
   pwd  # Should show /path/to/Aiwork
   ls examples/agents/document_processor/run.py  # Should exist
   ```

2. **Verify package is installed:**
   ```bash
   python -c "import aiwork; print(aiwork.__version__)"
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

### Slow Execution

The simulated example runs very fast (~0.001s). If execution is slow:

1. Check for network issues (if using real LLM APIs)
2. Verify no heavy dependencies are being loaded
3. Use `time` to profile: `time python examples/agents/document_processor/run.py`

### Import Errors After Updates

If you get import errors after pulling updates:

```bash
# Reinstall in development mode
pip install -e . --force-reinstall
```

## Next Steps

1. **Read the detailed README**: `examples/agents/document_processor/README.md`
2. **Explore the code**: Review `run.py` to understand implementation
3. **Try the other example**: `examples/agents/customer_support/run.py`
4. **Build your own**: Use this as a template for your use case
5. **Read the docs**: See `docs/USER_GUIDE.md` for comprehensive tutorial

## Related Documentation

- [User Guide](../../../docs/USER_GUIDE.md) - Complete framework tutorial
- [Architecture](../../../docs/ARCHITECTURE.md) - Technical design details
- [API Reference](../../../docs/API_REFERENCE.md) - Complete API documentation
- [Document Processor README](README.md) - Detailed architecture explanation

## Support

- **Issues**: [GitHub Issues](https://github.com/JayeshCC/Aiwork/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JayeshCC/Aiwork/discussions)
- **Examples**: Browse `examples/` directory for more patterns
