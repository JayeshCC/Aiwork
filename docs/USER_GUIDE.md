# AIWork User Guide

AIWork is an alpha-stage Python framework for learning and experimenting with agentic workflow orchestration. This guide focuses on implemented local behavior.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Build a DAG Workflow

```python
from aiwork.core.flow import Flow
from aiwork.core.task import Task
from aiwork.orchestrator import Orchestrator

def extract(context):
    return {"text": "invoice text"}

def classify(context):
    text = context["outputs"]["extract"]["text"]
    return {"category": "invoice", "text": text}

flow = Flow("classification_demo")
flow.add_task(Task("extract", extract))
flow.add_task(Task("classify", classify), depends_on=["extract"])

result = Orchestrator().execute(flow, {})
print(result["outputs"])
```

`Flow` resolves dependencies before execution. The local orchestrator then runs tasks sequentially.

## Inject Tasks Dynamically

```python
from aiwork.core.task import Task

def audit(context):
    return {"audit": "complete"}

def analyze(context):
    result = {"analyzed": True}
    if context["amount"] > 1000:
        result["next_tasks"] = [Task("audit", audit)]
    return result
```

Tasks returned through `next_tasks` are appended to the local execution queue.

## Use an Agent

```python
from aiwork.core.agent import Agent
from aiwork.core.task import Task

agent = Agent(
    role="Reviewer",
    goal="Summarize submitted material",
    backstory="A concise document reviewer",
    verbose=False,
)

task = Task("review", description="Review the document", agent=agent)
```

Without an LLM, the agent uses deterministic fallback output. An optional LLM can be supplied explicitly.

## Use Memory

```python
from aiwork.core.memory import VectorMemory

memory = VectorMemory()
memory.add("Customer prefers email updates")
matches = memory.search("email")
```

`VectorMemory` is local and lightweight. It uses word-overlap similarity rather than embeddings.

## Add Guardrails

```python
from aiwork.core.guardrail import Guardrail
from aiwork.core.task import Task

positive_amount = Guardrail(
    "positive_amount",
    lambda result: result.get("amount", 0) > 0,
)

task = Task(
    "calculate",
    lambda context: {"amount": 10},
    guardrails=[positive_amount],
)
```

Tasks support input and output guardrails. Guardrail failures participate in retry handling.

## Register Tools

```python
from aiwork.tools.registry import ToolRegistry

registry = ToolRegistry()
registry.register("normalize", lambda value: value.strip().lower())
normalize = registry.get_tool("normalize")
```

## Export an Airflow DAG

```python
from aiwork.integrations.airflow_exporter import AirflowExporter

AirflowExporter.export(flow, "classification_demo_dag.py")
```

The exporter writes task structure and dependencies. Generated task callables are placeholders and must be replaced for a real Airflow deployment.

## Run the Local Flask Demo

```bash
python -m aiwork.api --host 127.0.0.1 --port 5000
```

Example request:

```bash
curl -X POST http://127.0.0.1:5000/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "name": "demo",
    "tasks": [
      {"name": "extract", "depends_on": []},
      {"name": "analyze", "depends_on": ["extract"]}
    ]
  }'
```

The Flask API is a local demonstration API. Submitted tasks use generic handlers, state is held in memory, and execution uses daemon threads.

## Run Reference Workflows

```bash
python examples/agents/document_processor/run.py
python examples/agents/customer_support/run.py
```

These examples are reference workflows, not packaged domain agents. The document processor uses simulated OCR behavior.

## Integration Boundaries

| Integration | Current behavior |
| --- | --- |
| OpenVINO | Placeholder adapter only; no acceleration or model inference |
| Kafka | Prototype adapter only; no broker connection |
| Redis | State-manager stub only; use local mode for demos |
| Airflow | Exports DAG structure with placeholder callables |

## Simulated Benchmark

`benchmarks/openvino_benchmark.py` uses predefined sleep durations. It demonstrates a benchmark script shape but does not report measured OpenVINO performance.

## Tests

```bash
pytest
```

## More Detail

- [Architecture](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Mock Implementations](MOCK_IMPLEMENTATIONS.md)
- [Roadmap](ROADMAP.md)
