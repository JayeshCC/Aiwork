# System Architecture

## Overview
AIWork is a modular, layered framework for defining agentic workflows as task flows and executing
them with dependency resolution, retries, and observability. The architecture mirrors the Intel
problem statement: ingress sources feed a flow orchestrator, which executes tasks via tools and
integrations, while maintaining state and metrics.

## High-Level Architecture

```
Ingress Layer (REST, Queue, CLI)
          |
          v
Orchestration Layer (Flow DAG + Orchestrator)
          |
          v
Execution Layer (Tasks, Agents, Tools, Guardrails)
          |
          v
State/Memory + Observability
          |
          v
Integrations (Kafka, Airflow Export, OpenVINO)
```

## Components

### 1) Ingress Layer
- **REST API** (`src/aiwork/api/server.py`): FastAPI entrypoint for defining and executing flows.
- **Queue Adapter** (`src/aiwork/integrations/kafka_adapter.py`): Stub adapter for Kafka messaging.
- **CLI/Examples** (`examples/`): Local execution entrypoints.

### 2) Orchestration Layer
- **Flow** (`src/aiwork/core/flow.py`): DAG of tasks with dependency edges.
- **Orchestrator** (`src/aiwork/orchestrator.py`): Resolves execution order and executes tasks
  sequentially, collecting outputs in a shared context.

### 3) Execution Layer
- **Task** (`src/aiwork/core/task.py`): Atomic unit of work with retry logic, status, and guardrails.
- **Agent** (`src/aiwork/core/agent.py`): Role-based execution with optional memory and tools.
- **Tool Registry** (`src/aiwork/tools/registry.py`): Register and retrieve callable tools by name.
- **Guardrails** (`src/aiwork/core/guardrail.py`): Validation policies applied to task outputs.

### 4) State and Memory
- **VectorMemory** (`src/aiwork/core/memory.py`): Simple in-memory similarity search for recall.
- **StateManager** (`src/aiwork/memory/state_manager.py`): Local state persistence stub
  (Redis is a placeholder).

### 5) Observability
- **Metrics** (`src/aiwork/core/observability.py`): In-process metrics registry.
- **Logger/Monitor** (`src/aiwork/observability/logger.py`): Logging and execution timing decorator.

### 6) Integrations and Optimization
- **KafkaAdapter** (`src/aiwork/integrations/kafka_adapter.py`): Stub for distributed messaging.
- **AirflowExporter** (`src/aiwork/integrations/airflow_exporter.py`): Exports a Flow to an Airflow DAG.
- **OpenVINOAdapter** (`src/aiwork/integrations/openvino_adapter.py`): Stub for Intel model
  optimization/inference.

## Data Flow
1) **Define** a `Flow` and add `Task` nodes with dependencies.
2) **Submit** the flow through an ingress path (API, queue, or local).
3) **Resolve** the DAG into a topological order.
4) **Execute** tasks sequentially:
   - Each task receives the shared context.
   - Outputs are stored in `context["outputs"]`.
   - Guardrails validate outputs and can fail the task.
   - Retries occur up to the configured limit.
5) **Return** the final context to the caller.

## Reference Agents (Examples)
- **Document Processor**: OCR simulation with OpenVINO adapter, analysis, and compliance task.
- **Customer Support Bot**: Intent -> search -> response flow with multi-turn context.

## Reliability and Observability
- **Retries**: Implemented at the task level.
- **Metrics**: Task durations recorded in the metrics registry.
- **Logging**: Central logger and monitor decorator for timing.

## Performance and Intel Optimization
- **OpenVINO Adapter**: Present as a stub interface for model optimization/inference.
- **Benchmarking**: Simulated benchmarks in `benchmarks/openvino_benchmark.py`.

## Limitations (Current)
- Kafka and OpenVINO integrations are stubs (print-only behavior).
- Orchestrator is sequential; parallel execution is future work.
- Redis state storage is not wired (local in-memory only).
