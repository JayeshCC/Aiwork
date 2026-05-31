# AIWork API Reference

This reference documents the alpha-stage public surface used by the included examples and tests.

## Core

### `Agent`

```python
Agent(
    role: str,
    goal: str,
    backstory: str,
    tools: list = None,
    memory = None,
    llm = None,
    verbose: bool = True,
)
```

`execute_task(task_description, context)` uses an optional LLM or a deterministic fallback response.

### `Task`

```python
Task(
    name: str,
    description: str = None,
    agent: Agent = None,
    handler = None,
    retries: int = 3,
    guardrails: list = None,
    input_guardrails: list = None,
    verbose: bool = False,
)
```

For backwards compatibility, `Task(name, handler)` is supported.

### `Flow`

```python
flow = Flow("example")
flow.add_task(task)
flow.add_task(next_task, depends_on=["task_name"])
ordered_tasks = flow.get_topological_sort()
```

`get_topological_sort()` returns dependency order and raises `ValueError` for invalid dependencies or cycles.

### `Orchestrator`

```python
orchestrator = Orchestrator(executor=None, state_manager=None)
result = orchestrator.execute(flow, initial_context={}, workflow_id=None)
```

The local orchestrator resolves DAG order, executes tasks, records state, and appends tasks returned in `next_tasks`.

## Tools and Guardrails

### `ToolRegistry`

```python
registry.register(name, tool)
tool = registry.get_tool(name)
names = registry.list_tools()
```

### `Guardrail`

```python
guardrail = Guardrail(name, validator, description="")
is_valid = guardrail.validate(data)
```

## Memory and State

### `VectorMemory`

```python
memory = VectorMemory()
memory.add(text, metadata=None)
matches = memory.search(query, k=3)
```

The current implementation is local word-overlap search.

### `StateManager`

```python
state = StateManager(use_redis=False)
state.set_workflow_status(workflow_id, status, name=None, error=None)
state.set_task_status(workflow_id, task_name, status, error=None)
state.update_task_output(workflow_id, task_name, output)
workflow = state.get_workflow_state(workflow_id)
status = state.get_task_status(workflow_id, task_name)
```

`use_redis=True` is a stub boundary and does not create a Redis connection.

## Integrations

### `AirflowExporter`

```python
AirflowExporter.export(flow, output_path)
```

Writes an Airflow DAG file containing task names, dependencies, and placeholder callables.

### `KafkaAdapter`

```python
kafka = KafkaAdapter(bootstrap_servers="localhost:9092")
kafka.produce_task(topic, task_payload)
tasks = kafka.consume_tasks(topic)
```

This is an interface prototype. It does not connect to Kafka.

### `OpenVINOAdapter`

```python
adapter = OpenVINOAdapter(model_path=None)
reference = adapter.optimize_model(model)
result = adapter.infer(inputs)
```

This is an interface prototype. It does not compile models, run inference, or accelerate workloads.

## Local Flask Demonstration API

Start the server:

```bash
python -m aiwork.api --host 127.0.0.1 --port 5000
```

Endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/workflow` | Submit a generic workflow definition |
| `GET` | `/workflow/<workflow_id>` | Get workflow state |
| `GET` | `/workflow/<workflow_id>/task/<task_name>` | Get task state |
| `GET` | `/task/<task_id>` | Legacy task lookup endpoint |

The server is intended for local demonstration only.
