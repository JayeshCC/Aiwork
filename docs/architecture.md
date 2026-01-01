# System Architecture

## Overview
AIWork is designed as a modular, layered architecture to support scalable and efficient agentic workflows.

## Components

### 1. Core Layer
- **Agent**: A role-based entity with a goal, backstory, and set of tools.
- **Task**: The atomic unit of execution. Contains logic, retry policies, and status tracking.
- **Flow**: Represents a workflow as a Directed Acyclic Graph (DAG). Manages dependencies between tasks.
- **Orchestrator**: The engine that traverses the Flow DAG, resolving dependencies and executing tasks in the correct order (topological sort).

### 2. Integration Layer
- **KafkaAdapter**: Facilitates asynchronous communication. Tasks can be pushed to Kafka topics for distributed workers to pick up.
- **OpenVINOAdapter**: Provides a unified interface for running ML models optimized with Intel OpenVINO.

### 3. Tooling Layer
- **ToolRegistry**: A central repository for registering and retrieving tools (functions) that agents can use.

## Data Flow
1. **Definition**: User defines a `Flow` and adds `Task` objects with dependencies.
2. **Submission**: The Flow is submitted to the `Orchestrator`.
3. **Resolution**: Orchestrator calculates the execution order.
4. **Execution**:
   - Tasks are executed sequentially or in parallel (future).
   - Context is passed from task to task.
   - ML tasks use `OpenVINOAdapter` for acceleration.
5. **Output**: Final context is returned to the user.

## Intel Optimizations
- **Inference**: All ML inference calls are routed through the OpenVINO adapter to ensure maximum throughput on Intel CPUs/GPUs.
- **Benchmarking**: Validated on Intel DevCloud (Xeon Scalable Processors).
