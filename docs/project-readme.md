# AIWork: Lightweight Agentic Framework

AIWork is a Python framework for orchestrating agentic workflows without relying on external agent
frameworks. It provides a small, readable core for Tasks, Flows, Agents, and Orchestration, with
stubs for Apache and Intel integrations.

## Key Features

| Feature | Description |
| --- | --- |
| Agent-Centric | Define agents with role, goal, and tools. |
| Task/Flow DAG | Compose workflows with dependencies. |
| Memory | VectorMemory for simple recall and context. |
| Guardrails | Validation hooks for task outputs. |
| Observability | Basic metrics registry and logging. |
| Integrations | Airflow export, Kafka/OpenVINO adapters (stubs). |

## Documentation

- User Guide: `docs/user-guide.md`
- Architecture: `docs/architecture.md`
- Deployment: `docs/deployment.md`
- Compliance Checklist: `docs/compliance-checklist.md`
- Problem Statement: `docs/INTEL problem 2.md`

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```python
from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

flow = Flow("hello_world")
flow.add_task(Task("step", lambda c: "ok"))

orchestrator = Orchestrator()
result = orchestrator.execute(flow, {})
print(result["outputs"])
```

## Notes

- Kafka and OpenVINO adapters are simulated (print-only behavior).
- DevCloud benchmark numbers are not generated in this repo.
