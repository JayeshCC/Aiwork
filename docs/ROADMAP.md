# AIWork Roadmap

AIWork is an alpha-stage portfolio project. The roadmap is intentionally undated: priorities should be driven by verified implementation work rather than stale release promises.

## Current Status

### Implemented Core

- Agent, task, flow, and orchestrator abstractions
- DAG dependency resolution with topological sorting
- Sequential local execution and dynamic task injection
- Input and output guardrails with retry handling
- Lightweight local memory
- In-memory workflow state tracking
- Tool registry
- Local Flask demonstration API
- Airflow DAG exporter
- Reference document-processing and customer-support workflows
- Automated tests

### Prototype or Stub Boundaries

- OpenVINO adapter: placeholder interface only
- Kafka adapter: mock producer and consumer behavior only
- Redis backend: interface stub; local state is the implemented mode
- Benchmark script: simulated timings only
- Flask API: local demonstration behavior, not a hardened service

## Priorities

### Validate Existing Core

- Keep the automated suite reliable
- Improve documentation examples so they match public APIs
- Add focused tests when workflow behavior changes
- Document limitations as part of each demo

### Replace Integration Prototypes

- Implement OpenVINO model loading, compilation, inference, and hardware-backed benchmarks
- Implement Kafka producer and consumer behavior against a real broker
- Implement Redis persistence and cross-process state tests
- Preserve adapter boundaries so these additions do not complicate local usage

### Strengthen Runtime Capabilities

- Add parallel execution for independent DAG branches
- Improve state persistence and recovery
- Expand observability
- Evaluate semantic-memory backends as optional integrations

### Prepare for Deployment Work

- Define supported deployment targets
- Add a reproducible container or packaging path before documenting container deployment
- Add authentication, rate limiting, durable storage, and worker management before describing the API as deployable
- Publish measured benchmarks only with hardware, workload, and methodology details

## Contribution Areas

The most useful contributions are real adapter implementations, reproducible integration tests, measured benchmark work, and small reference workflows that demonstrate verified framework behavior.
