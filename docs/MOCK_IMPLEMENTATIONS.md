# Mock Implementations and Alpha-Stage Boundaries

This document records which parts of AIWork are implemented and which parts are prototypes or stubs. The distinction matters because the repository is an alpha-stage portfolio project, not a production system.

## Status Summary

| Component | Status | What is verified |
| --- | --- | --- |
| `Flow` | Implemented core | Stores dependencies and resolves DAG order |
| `Orchestrator` | Implemented core | Executes local tasks sequentially and injects runtime tasks |
| `Task` and local executor | Implemented core | Runs handlers or agents with guardrails and retry behavior |
| `Agent` | Implemented core | Supports role metadata, tools, optional memory, optional LLM, and deterministic fallback |
| `VectorMemory` | Implemented core | Local word-overlap search |
| `ToolRegistry` | Implemented core | Registers and retrieves reusable tools |
| `StateManager` local mode | Implemented core | Tracks state in memory for the running process |
| Flask API | Demonstration API | Submits generic workflow definitions and reports in-memory status |
| Airflow exporter | Implemented adapter | Writes DAG structure with placeholder Python callables |
| Kafka adapter | Interface prototype | Prints produced payloads and yields hard-coded mock tasks |
| Redis mode | Interface stub | Does not connect to Redis or persist distributed state |
| OpenVINO adapter | Interface prototype | Returns placeholder optimization and inference values |
| Benchmark script | Simulation | Compares intentionally delayed mock functions |

## OpenVINO Prototype

`src/aiwork/integrations/openvino_adapter.py` does not import the OpenVINO runtime, compile models, perform inference, or use Intel hardware acceleration. Its return values are placeholders that exercise an adapter shape.

`benchmarks/openvino_benchmark.py` uses `time.sleep()` calls to simulate two timing paths. Results from that script are simulated and must not be cited as measured performance.

## Kafka Prototype

`src/aiwork/integrations/kafka_adapter.py` does not connect to a broker. `produce_task()` prints a payload and `consume_tasks()` yields a fixed list of mock tasks. The module demonstrates where a real messaging implementation could fit.

## Redis Stub

`StateManager(use_redis=True)` does not create a Redis client. The working backend is local in-memory state. That mode is useful for demos and tests but is ephemeral and process-local.

## Local Flask Demonstration API

The Flask API is useful for demonstrating ingress and state reporting. It is intentionally limited:

- submitted JSON tasks use a generic handler
- state is held in memory
- work is run in daemon threads
- there is no durable queue
- it is not a hardened deployment target

## Reference Workflows

The document processor and customer-support examples are reference workflows. They show composition patterns such as dependency ordering, memory use, guardrails, and dynamic task injection. They are not packaged domain agents and should not be described as deployment-grade automation.

## Benchmark Reporting Rule

Do not publish a performance number until it is measured against a real implementation with a documented model, workload, hardware configuration, software versions, and reproducible command.
