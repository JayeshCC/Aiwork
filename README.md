# AIWork - Build-Your-Own AI Agent Framework

AIWork is a lightweight Python framework for defining and executing agentic workflows as task flows
without relying on existing agent frameworks. It targets the Intel AI Innovation Challenge Problem 2
requirements and provides a minimal, understandable core with extensible integrations.

## Problem Statement Alignment

| Requirement | Status |
| --- | --- |
| Define and execute task flows (DAG) | Implemented (`Flow`, `Orchestrator`) |
| Input handlers, tools/actions, output actions | Implemented (`Task` handlers, `ToolRegistry`) |
| Memory, guardrails, observability | Implemented (`VectorMemory`, `Guardrail`, metrics) |
| Ingress (REST/queue) | REST API implemented, queue adapter stubbed |
| Apache components for messaging/orchestration | Kafka adapter stub, Airflow DAG exporter |
| Intel tech (OpenVINO optimization) | OpenVINO adapter stub, benchmark simulation |
| Two reference agents | Implemented (document processor, customer support) |
| Benchmarks (pre/post optimization) | Simulated benchmark script |

## Project Structure

```
.
├── benchmarks/                 # Benchmark scripts (simulated OpenVINO timings)
├── docs/                       # Specs, guides, architecture, compliance
├── examples/                   # Reference agents and demos
├── scripts/                    # Setup helpers
├── src/aiwork/                 # Framework source (package root)
├── tests/                      # Unit and integration tests
├── requirements.txt
└── README.md
```

## Core Concepts

- Agent: role-based actor with optional memory and tools.
- Task: atomic unit of work with retries and optional guardrails.
- Flow: DAG of tasks and dependencies.
- Orchestrator: executes flows and manages outputs.
- Tool Registry: shared registry for callable tools.
- Observability: simple metrics registry and logging helpers.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the quickstart demo:

```bash
python examples/quickstart.py
```

## Reference Agents

- Document Processor: `examples/agents/document_processor/run.py`
- Customer Support Bot: `examples/agents/customer_support/run.py`

## REST API

The FastAPI server exposes basic flow execution:

```bash
python -m aiwork.api.server
```

## Benchmarks

The OpenVINO benchmark script is simulated for latency comparisons:

```bash
python benchmarks/openvino_benchmark.py
```

## Testing

```bash
pytest
```

## Notes and Limitations

- Kafka/OpenVINO integrations are stubs (print-only behavior).
- DevCloud benchmarking is not automated in this repo.
- Orchestrator executes sequentially; parallel execution is not implemented.

## Documentation

- Problem statement: `docs/INTEL problem 2.md`
- Legacy spec: `docs/intel.txt`
- Architecture: `docs/architecture.md`
- User guide: `docs/user-guide.md`
- Deployment: `docs/deployment.md`
- Compliance checklist: `docs/compliance-checklist.md`
