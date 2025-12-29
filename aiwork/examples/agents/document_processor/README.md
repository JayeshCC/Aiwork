# Document Processor Agent

This example demonstrates an **Agent-Centric** workflow using **Hybrid Orchestration**.

## Key Concepts

1.  **Agents**: Specialized entities with a Role, Goal, and Backstory.
    *   **Document Processor**: Uses OpenVINO tools to extract text.
    *   **Financial Analyst**: Analyzes text for insights.
    *   **Compliance Officer**: Enforces policies.

2.  **Hybrid Orchestration**:
    *   **Static Flow**: The initial pipeline is defined as a DAG (OCR -> Analyze).
    *   **Dynamic Flow**: The `Analyze` task can dynamically create and inject a new `Audit` task into the workflow based on runtime data (e.g., High value invoice).

## How to Run

```bash
python run.py
```

## Expected Output

The agent will process a simulated invoice. If the amount exceeds $1000, you will see a dynamic "Compliance Check" task being triggered and executed.
