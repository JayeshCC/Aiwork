# 📖 AIWork API Reference

Complete API documentation for all public classes, methods, and endpoints in the AIWork framework.

---

## Table of Contents

1. [Core Classes](#core-classes)
2. [Orchestration](#orchestration)
3. [Integrations](#integrations)
4. [Memory & State](#memory--state)
5. [Tools & Guardrails](#tools--guardrails)
6. [REST API](#rest-api)
7. [Observability](#observability)

---

## Core Classes

### Agent

Represents an autonomous AI worker with a specific role and capabilities.

```python
from aiwork.core.agent import Agent
```

#### Constructor

```python
Agent(
    role: str,
    goal: str,
    backstory: str,
    tools: List[Any] = None,
    memory: Any = None,
    llm: Any = None,
    verbose: bool = True
)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `role` | `str` | Yes | The agent's job title or identity (e.g., "Data Analyst") |
| `goal` | `str` | Yes | Primary objective the agent is trying to achieve |
| `backstory` | `str` | Yes | Context that guides the agent's behavior and decision-making |
| `tools` | `List[Any]` | No | List of functions/tools the agent can use (default: `[]`) |
| `memory` | `VectorMemory` | No | Memory system for storing and recalling context (default: `None`) |
| `llm` | `Any` | No | LLM integration placeholder for future use (default: `None`) |
| `verbose` | `bool` | No | Whether to print agent's thinking process (default: `True`) |

**Returns:** `Agent` instance

**Example:**

```python
from aiwork.core.agent import Agent
from aiwork.core.memory import VectorMemory

# Create memory
memory = VectorMemory()
memory.add("User prefers detailed explanations")

# Create agent
analyst = Agent(
    role="Financial Analyst",
    goal="Detect fraud in transactions",
    backstory="20 years of experience in fraud detection",
    tools=[calculator_tool, database_tool],
    memory=memory,
    verbose=True
)
```

#### Methods

##### `execute_task()`

Executes a task using the agent's persona and tools.

```python
agent.execute_task(
    task_description: str,
    context: Dict[str, Any]
) -> Any
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_description` | `str` | Description of what needs to be done |
| `context` | `Dict[str, Any]` | Execution context with inputs and outputs |

**Returns:** `Any` - Result of the task execution

**Example:**

```python
context = {
    "outputs": {"previous_task": {"data": "invoice.pdf"}},
    "inputs": {"user_id": "123"}
}

result = analyst.execute_task(
    "Analyze this invoice for potential fraud",
    context
)
```

**Notes:**
- Automatically searches memory for relevant context
- Prints thinking process if `verbose=True`
- Returns formatted result string by default

---

### Task

Atomic unit of work with retry logic and validation.

```python
from aiwork.core.task import Task
```

#### Constructor

```python
Task(
    name: str,
    description: Optional[str] = None,
    agent: Optional[Agent] = None,
    handler: Callable[[Dict[str, Any]], Any] = None,
    retries: int = 3,
    guardrails: List[Guardrail] = None
)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Unique identifier for the task |
| `description` | `str` | No | Human-readable description of what the task does |
| `agent` | `Agent` | No | Agent assigned to execute this task (default: `None`) |
| `handler` | `Callable` | Yes* | Function that executes the task logic |
| `retries` | `int` | No | Maximum number of retry attempts on failure (default: `3`) |
| `guardrails` | `List[Guardrail]` | No | Output validation rules (default: `[]`) |

**Returns:** `Task` instance

**Notes:**
- *Either `agent` or `handler` must be provided
- If both provided, handler is used with agent's context
- Supports backward compatibility: `Task(name, handler)` works

**Example:**

```python
from aiwork.core.task import Task
from aiwork.core.guardrail import Guardrail

# Create handler function
def extract_text(ctx):
    doc = ctx.get("document")
    # Perform OCR extraction
    return {"text": "Extracted content..."}

# Create guardrail
def validate_text(output):
    return len(output.get("text", "")) > 0

text_guard = Guardrail("non_empty_text", validate_text)

# Create task
task = Task(
    name="extract",
    description="Extract text from document",
    handler=extract_text,
    retries=3,
    guardrails=[text_guard]
)
```

#### Methods

##### `execute()`

Executes the task with retry logic and guardrail validation.

```python
task.execute(context: Dict[str, Any]) -> Any
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `Dict[str, Any]` | Execution context containing inputs and outputs from previous tasks |

**Returns:** `Any` - Task execution result

**Raises:**
- `ValueError`: If task has no agent and no handler
- `Exception`: If all retry attempts fail

**Example:**

```python
context = {
    "inputs": {"document": "invoice.pdf"},
    "outputs": {}
}

result = task.execute(context)
print(result)  # {"text": "Extracted content..."}
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `str` | Unique UUID for the task instance |
| `name` | `str` | Task name |
| `description` | `str` | Task description |
| `status` | `str` | Current status: `"PENDING"`, `"RUNNING"`, `"COMPLETED"`, `"FAILED"` |
| `output` | `Any` | Result of successful execution (or `None`) |
| `error` | `str` | Error message if failed (or `None`) |

---

### Flow

Represents a workflow as a Directed Acyclic Graph (DAG) of tasks.

```python
from aiwork.core.flow import Flow
```

#### Constructor

```python
Flow(name: str)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Unique identifier for the flow |

**Returns:** `Flow` instance

**Example:**

```python
from aiwork.core.flow import Flow

flow = Flow("document_processing_pipeline")
```

#### Methods

##### `add_task()`

Adds a task to the flow with optional dependencies.

```python
flow.add_task(
    task: Task,
    depends_on: List[str] = None
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task` | `Task` | Task instance to add |
| `depends_on` | `List[str]` | List of task names this task depends on (default: `[]`) |

**Returns:** `None`

**Raises:**
- `ValueError`: If task with same name already exists

**Example:**

```python
from aiwork.core.task import Task

# Create tasks
extract_task = Task("extract", extract_handler)
validate_task = Task("validate", validate_handler)
store_task = Task("store", store_handler)

# Build flow
flow.add_task(extract_task)
flow.add_task(validate_task, depends_on=["extract"])
flow.add_task(store_task, depends_on=["validate"])

# Execution order: extract → validate → store
```

##### `get_topological_sort()`

Returns tasks in execution order based on dependencies.

```python
flow.get_topological_sort() -> List[Task]
```

**Returns:** `List[Task]` - Ordered list of tasks

**Raises:**
- `ValueError`: If cycle detected in DAG

**Example:**

```python
execution_order = flow.get_topological_sort()
for task in execution_order:
    print(task.name)
# Output: extract, validate, store
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Flow name |
| `tasks` | `Dict[str, Task]` | Dictionary of task name to Task instance |
| `dependencies` | `Dict[str, Set[str]]` | Dependency graph: task name to set of dependency names |

---

## Orchestration

### Orchestrator

Execution engine that runs flows with dependency resolution.

```python
from aiwork.orchestrator import Orchestrator
```

#### Constructor

```python
Orchestrator()
```

**Parameters:** None

**Returns:** `Orchestrator` instance

**Example:**

```python
from aiwork.orchestrator import Orchestrator

orchestrator = Orchestrator()
```

#### Methods

##### `execute()`

Executes a flow with initial context.

```python
orchestrator.execute(
    flow: Flow,
    initial_context: Dict[str, Any] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `flow` | `Flow` | Flow instance to execute |
| `initial_context` | `Dict[str, Any]` | Initial inputs for the flow (default: `{}`) |

**Returns:** `Dict[str, Any]` - Final context with all task outputs

**Context Structure:**

```python
{
    "inputs": {
        # Original initial_context data
    },
    "outputs": {
        "task_name": {result},
        "another_task": {result},
        ...
    }
}
```

**Example:**

```python
# Execute flow
result = orchestrator.execute(
    flow=my_flow,
    initial_context={
        "document_id": "DOC-12345",
        "user_id": "user@example.com"
    }
)

# Access results
print(result["outputs"]["extract"])
print(result["outputs"]["analyze"])
print(result["outputs"]["store"])
```

**Notes:**
- Executes tasks in topological order
- Handles retry logic per task
- Supports dynamic task injection (hybrid orchestration)
- Prints execution progress if tasks/agents are verbose

---

## Integrations

### OpenVINOAdapter

Interface for Intel® OpenVINO™ model optimization and inference.

```python
from aiwork.integrations.openvino_adapter import OpenVINOAdapter
```

#### Constructor

```python
OpenVINOAdapter(model_path: str = None)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_path` | `str` | Path to OpenVINO IR model (.xml file) |

**Returns:** `OpenVINOAdapter` instance

**Example:**

```python
adapter = OpenVINOAdapter(model_path="models/distilbert.xml")
```

#### Methods

##### `optimize_model()`

Optimizes a model using OpenVINO (stub implementation).

```python
adapter.optimize_model(model: Any) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `Any` | Model to optimize (PyTorch, TensorFlow, etc.) |

**Returns:** `str` - Reference to optimized model

**Example:**

```python
pytorch_model = load_pytorch_model()
optimized_ref = adapter.optimize_model(pytorch_model)
```

##### `infer()`

Runs inference on inputs using optimized model.

```python
adapter.infer(inputs: dict) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `inputs` | `dict` | Input tensors/data for the model |

**Returns:** `dict` - Inference results with speedup information

**Example:**

```python
result = adapter.infer({
    "input_ids": [101, 2003, 102],
    "attention_mask": [1, 1, 1]
})

print(result)
# {"result": "inference_complete", "speedup": "3.7x"}
```

**Note:** Current implementation is a stub. Real OpenVINO integration requires:
```bash
pip install openvino
```

---

### KafkaAdapter

Interface for Apache Kafka distributed messaging.

```python
from aiwork.integrations.kafka_adapter import KafkaAdapter
```

#### Constructor

```python
KafkaAdapter(bootstrap_servers: str = "localhost:9092")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `bootstrap_servers` | `str` | Kafka broker addresses (default: `"localhost:9092"`) |

**Returns:** `KafkaAdapter` instance

**Example:**

```python
kafka = KafkaAdapter(bootstrap_servers="kafka1:9092,kafka2:9092")
```

#### Methods

##### `produce_task()`

Sends a task to a Kafka topic.

```python
kafka.produce_task(
    topic: str,
    task_payload: dict
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | `str` | Kafka topic name |
| `task_payload` | `dict` | Task data to send |

**Returns:** `None`

**Example:**

```python
kafka.produce_task("aiwork.tasks", {
    "task_id": "task-001",
    "flow_name": "process_document",
    "context": {"document_id": "DOC-123"}
})
```

##### `consume_tasks()`

Generator that yields tasks from a Kafka topic.

```python
kafka.consume_tasks(topic: str) -> Iterator[dict]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | `str` | Kafka topic to subscribe to |

**Returns:** `Iterator[dict]` - Generator of task payloads

**Example:**

```python
for task in kafka.consume_tasks("aiwork.tasks"):
    print(f"Processing task: {task['task_id']}")
    # Process task...
```

**Note:** Current implementation is a stub. Real Kafka integration requires:
```bash
pip install confluent-kafka
```

---

### AirflowExporter

Exports AIWork flows to Apache Airflow DAG files.

```python
from aiwork.integrations.airflow_exporter import AirflowExporter
```

#### Constructor

```python
AirflowExporter()
```

**Returns:** `AirflowExporter` instance

#### Methods

##### `export_flow()`

Converts an AIWork Flow to Airflow DAG Python code.

```python
exporter.export_flow(
    flow: Flow,
    output_path: str = None
) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `flow` | `Flow` | Flow to export |
| `output_path` | `str` | Optional file path to write DAG code |

**Returns:** `str` - Generated Airflow DAG code

**Example:**

```python
from aiwork.integrations.airflow_exporter import AirflowExporter

exporter = AirflowExporter()
dag_code = exporter.export_flow(my_flow, "dags/my_flow_dag.py")
print(dag_code)
```

---

## Memory & State

### VectorMemory

Simple similarity-based memory for agent context storage.

```python
from aiwork.core.memory import VectorMemory
```

#### Constructor

```python
VectorMemory()
```

**Parameters:** None

**Returns:** `VectorMemory` instance

**Example:**

```python
memory = VectorMemory()
```

#### Methods

##### `add()`

Stores a text string in memory.

```python
memory.add(text: str)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Text to store in memory |

**Returns:** `None`

**Example:**

```python
memory.add("Customer prefers email communication")
memory.add("Customer is in premium tier")
memory.add("Last order was placed on 2024-01-15")
```

##### `search()`

Searches memory for relevant context using similarity.

```python
memory.search(
    query: str,
    top_k: int = 3
) -> List[dict]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | Search query |
| `top_k` | `int` | Number of results to return (default: `3`) |

**Returns:** `List[dict]` - List of matching memories with scores

**Result Format:**
```python
[
    {"text": "relevant memory 1", "score": 0.95},
    {"text": "relevant memory 2", "score": 0.87},
    {"text": "relevant memory 3", "score": 0.72}
]
```

**Example:**

```python
results = memory.search("customer communication preferences", top_k=2)
for result in results:
    print(f"Score: {result['score']:.2f} - {result['text']}")
# Output:
# Score: 0.95 - Customer prefers email communication
# Score: 0.72 - Customer is in premium tier
```

**Note:** Uses simple TF-IDF similarity. For semantic search, integrate embedding models.

---

### StateManager

Manages state persistence for workflows.

```python
from aiwork.memory.state_manager import StateManager
```

#### Constructor

```python
StateManager(
    use_redis: bool = False,
    redis_url: str = "redis://localhost:6379"
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `use_redis` | `bool` | Whether to use Redis for distributed state (default: `False`) |
| `redis_url` | `str` | Redis connection URL (default: `"redis://localhost:6379"`) |

**Returns:** `StateManager` instance

**Example:**

```python
# Local state
state = StateManager()

# Redis state
state = StateManager(
    use_redis=True,
    redis_url="redis://prod-redis:6379"
)
```

#### Methods

##### `save_state()`

Saves workflow state.

```python
state.save_state(
    flow_id: str,
    state_data: dict
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `flow_id` | `str` | Unique identifier for the flow |
| `state_data` | `dict` | State data to persist |

**Returns:** `None`

**Example:**

```python
state.save_state("flow-123", {
    "status": "running",
    "completed_tasks": ["extract", "validate"],
    "current_task": "analyze",
    "context": {...}
})
```

##### `get_state()`

Retrieves workflow state.

```python
state.get_state(flow_id: str) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `flow_id` | `str` | Flow identifier |

**Returns:** `dict` - Saved state or empty dict if not found

**Example:**

```python
saved = state.get_state("flow-123")
if saved:
    print(f"Resuming from task: {saved['current_task']}")
```

---

## Tools & Guardrails

### ToolRegistry

Centralized registry for reusable tools.

```python
from aiwork.tools.registry import ToolRegistry, registry
```

#### Using the Global Registry

```python
from aiwork.tools.registry import registry

# Register a tool
@registry.register("calculator")
def calculator(x, y, op):
    if op == "add":
        return x + y
    elif op == "multiply":
        return x * y

# Get a tool
calc = registry.get_tool("calculator")
result = calc(5, 3, "add")  # 8

# List tools
tools = registry.list_tools()
print(tools)  # ["calculator"]
```

#### Methods

##### `register()`

Decorator to register a function as a tool.

```python
@registry.register(name: str)
def tool_function(...):
    ...
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique tool identifier |

**Example:**

```python
@registry.register("search")
def web_search(query):
    # Implementation
    return {"results": [...]}
```

##### `get_tool()`

Retrieves a registered tool.

```python
registry.get_tool(name: str) -> Callable
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Tool name |

**Returns:** `Callable` - The registered function

**Raises:**
- `ValueError`: If tool not found

##### `list_tools()`

Lists all registered tools.

```python
registry.list_tools() -> List[str]
```

**Returns:** `List[str]` - List of tool names

---

### Guardrail

Validates task outputs for compliance and quality.

```python
from aiwork.core.guardrail import Guardrail
```

#### Constructor

```python
Guardrail(
    name: str,
    validator: Callable[[Any], bool],
    description: str = ""
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique identifier for the guardrail |
| `validator` | `Callable` | Function that returns `True` if valid, `False` otherwise |
| `description` | `str` | Human-readable description (default: `""`) |

**Returns:** `Guardrail` instance

**Example:**

```python
def check_positive_amount(output):
    return output.get("amount", 0) > 0

amount_guard = Guardrail(
    name="positive_amount",
    validator=check_positive_amount,
    description="Ensures transaction amount is positive"
)
```

#### Methods

##### `validate()`

Validates data against the guardrail.

```python
guardrail.validate(data: Any) -> bool
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `Any` | Data to validate |

**Returns:** `bool` - `True` if valid, `False` if invalid or exception

**Example:**

```python
output = {"amount": 100.50, "currency": "USD"}
is_valid = amount_guard.validate(output)
print(is_valid)  # True

output = {"amount": -50, "currency": "USD"}
is_valid = amount_guard.validate(output)
print(is_valid)  # False
```

**Common Guardrail Patterns:**

```python
# Email validation
email_guard = Guardrail(
    "valid_email",
    lambda x: "@" in x.get("email", ""),
    "Validates email format"
)

# Range check
range_guard = Guardrail(
    "amount_range",
    lambda x: 0 < x.get("amount", 0) < 100000,
    "Amount must be between $0 and $100k"
)

# Required fields
def check_required(data):
    required = ["name", "email", "amount"]
    return all(field in data for field in required)

required_guard = Guardrail(
    "required_fields",
    check_required,
    "Ensures all required fields present"
)
```

---

## REST API

The AIWork REST API provides HTTP endpoints for flow execution.

### Starting the Server

```bash
python -m aiwork.api.server
```

Server runs on `http://localhost:8000` by default.

### Endpoints

#### Health Check

**`GET /`**

Check if the server is running.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "healthy",
  "framework": "AIWork"
}
```

**Status Code:** `200 OK`

---

#### Execute Flow

**`POST /execute`**

Execute a workflow defined in JSON.

**Request Body:**

```json
{
  "flow_name": "string",
  "tasks": [
    {
      "name": "string",
      "depends_on": ["string"]
    }
  ],
  "input_context": {
    "key": "value"
  }
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "flow_name": "document_pipeline",
    "tasks": [
      {"name": "extract"},
      {"name": "analyze", "depends_on": ["extract"]},
      {"name": "store", "depends_on": ["analyze"]}
    ],
    "input_context": {
      "document_id": "DOC-12345",
      "user_id": "user@example.com"
    }
  }'
```

**Response:**

```json
{
  "status": "success",
  "outputs": {
    "extract": {
      "text": "..."
    },
    "analyze": {
      "insights": "..."
    },
    "store": {
      "stored": true
    }
  }
}
```

**Status Codes:**
- `200 OK`: Flow executed successfully
- `500 Internal Server Error`: Execution failed

**Error Response:**

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Notes:**
- Task handlers are mocked in the API (returns `{"status": "executed"}`)
- In production, integrate with ToolRegistry for real handlers
- Supports all Flow and Task features (dependencies, retries, etc.)

---

## Observability

### Metrics Registry

Collects and stores execution metrics.

```python
from aiwork.core.observability import metrics
```

#### Methods

##### `record()`

Records a metric value.

```python
metrics.record(
    name: str,
    value: float,
    tags: dict = None
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Metric name |
| `value` | `float` | Metric value |
| `tags` | `dict` | Optional tags for grouping (default: `{}`) |

**Example:**

```python
import time
from aiwork.core.observability import metrics

start = time.time()
# ... do work ...
duration = time.time() - start

metrics.record("task_duration_seconds", duration, {
    "task": "extract",
    "status": "success"
})
```

##### `get()`

Retrieves recorded metrics.

```python
metrics.get(name: str) -> List[dict]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Metric name |

**Returns:** `List[dict]` - List of recorded metrics

**Example:**

```python
task_metrics = metrics.get("task_duration_seconds")
for metric in task_metrics:
    print(f"Task: {metric['tags']['task']}")
    print(f"Duration: {metric['value']:.2f}s")
    print(f"Status: {metric['tags']['status']}")
```

**Built-in Metrics:**

| Metric | Description | Tags |
|--------|-------------|------|
| `task_duration_seconds` | Task execution time | `task`, `status` |

---

## Complete Example

Here's a complete example using multiple API components:

```python
from aiwork.core.agent import Agent
from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.core.memory import VectorMemory
from aiwork.core.guardrail import Guardrail
from aiwork.orchestrator import Orchestrator
from aiwork.integrations.openvino_adapter import OpenVINOAdapter
from aiwork.core.observability import metrics

# Setup memory
memory = VectorMemory()
memory.add("Customer prefers technical details")
memory.add("Customer is a Python developer")

# Setup tools
ov_adapter = OpenVINOAdapter("models/classifier.xml")

# Create agent
analyst = Agent(
    role="Technical Analyst",
    goal="Analyze documents with ML models",
    backstory="Expert in ML and data analysis",
    tools=[ov_adapter],
    memory=memory
)

# Create handlers
def classify_document(ctx):
    doc = ctx["inputs"]["document"]
    result = ov_adapter.infer({"doc": doc})
    return {"category": "technical", "confidence": 0.95}

def generate_report(ctx):
    category = ctx["outputs"]["classify"]["category"]
    confidence = ctx["outputs"]["classify"]["confidence"]
    return {
        "report": f"Document classified as {category} with {confidence:.0%} confidence"
    }

# Create guardrails
confidence_guard = Guardrail(
    "high_confidence",
    lambda x: x.get("confidence", 0) > 0.8,
    "Requires confidence > 80%"
)

# Build flow
flow = Flow("document_analysis")

classify_task = Task(
    name="classify",
    description="Classify document type",
    agent=analyst,
    handler=classify_document,
    retries=2,
    guardrails=[confidence_guard]
)

report_task = Task(
    name="report",
    description="Generate analysis report",
    agent=analyst,
    handler=generate_report,
    retries=1
)

flow.add_task(classify_task)
flow.add_task(report_task, depends_on=["classify"])

# Execute
orchestrator = Orchestrator()
result = orchestrator.execute(flow, {
    "document": "technical_spec.pdf"
})

# Check results
print(result["outputs"]["report"])

# Check metrics
task_metrics = metrics.get("task_duration_seconds")
total_time = sum(m["value"] for m in task_metrics)
print(f"Total execution time: {total_time:.2f}s")
```

---

## Type Signatures

For type checking and IDE support:

```python
from typing import Any, Callable, Dict, List, Optional, Set

# Common type aliases
Context = Dict[str, Any]
TaskHandler = Callable[[Context], Any]
ValidatorFunc = Callable[[Any], bool]
```

---

## Error Handling

All components follow consistent error handling:

```python
try:
    result = orchestrator.execute(flow, context)
except ValueError as e:
    # Configuration error (missing handler, cycle in DAG, etc.)
    print(f"Configuration error: {e}")
except Exception as e:
    # Execution error (task failed after retries)
    print(f"Execution failed: {e}")
```

---

## Best Practices

1. **Type Hints**: Use type hints for better IDE support
2. **Error Handling**: Always handle potential errors in task handlers
3. **Guardrails**: Add guardrails for critical validations
4. **Retries**: Set appropriate retry counts based on task reliability
5. **Logging**: Use `verbose=True` during development for debugging
6. **Metrics**: Collect metrics for production monitoring
7. **Memory**: Use memory for agents that need context awareness
8. **Tools**: Register reusable tools in the ToolRegistry

---

## Version Compatibility

- **Python**: 3.8+
- **FastAPI**: 0.104.1+
- **NumPy**: 1.26.2+

For optional integrations:
- **OpenVINO**: 2024.0+ (not installed by default)
- **Kafka**: confluent-kafka 2.3.0+ (not installed by default)
- **Redis**: redis 5.0.1+ (installed, but optional to use)

---

## See Also

- [User Guide](USER_GUIDE.md) - Tutorials and examples
- [Architecture](ARCHITECTURE.md) - System design
- [Deployment](DEPLOYMENT.md) - Production deployment
- [Benchmarks](BENCHMARKS.md) - Performance data

---

<div align="center">
  <sub>Built with ❤️ for the Intel AI Innovation Challenge 2024</sub>
</div>
