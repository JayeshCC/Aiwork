# 🚀 Production Migration Guide

## 📋 Overview

This guide provides **step-by-step instructions** for migrating AIWork stub implementations to production-ready versions. Whether you're preparing for production deployment or contributing to the project, this guide shows you exactly how to implement real integrations.

**Target Audience**:
- Developers preparing AIWork for production use
- Contributors implementing Phase 1 features
- DevOps engineers deploying AIWork
- Anyone needing to understand implementation details

---

## Table of Contents

1. [OpenVINO Migration](#1-openvino-migration)
2. [Kafka Migration](#2-kafka-migration)
3. [Redis Migration](#3-redis-migration)
4. [Docker Deployment](#4-docker-deployment)
5. [Performance Tuning](#5-performance-tuning)
6. [Production Configuration](#6-production-configuration)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. OpenVINO Migration

### 📖 Understanding the Current Stub

**Current Implementation** (`src/aiwork/integrations/openvino_adapter.py`):
```python
class OpenVINOAdapter:
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        print(f"Initialized OpenVINO Adapter for model: {model_path}")

    def optimize_model(self, model):
        print("Optimizing model with OpenVINO...")
        return "OPTIMIZED_MODEL_REF"

    def infer(self, inputs):
        print(f"Running OpenVINO inference on inputs: {inputs}")
        return {"result": "inference_complete", "speedup": "3.7x"}
```

**What's Missing**:
- Real OpenVINO runtime integration
- Model compilation and optimization
- Actual inference execution
- Hardware-specific optimizations
- Error handling and validation

---

### 🔧 Step 1: Install OpenVINO Toolkit

**Option A: pip install (Recommended)**
```bash
# Install OpenVINO runtime
pip install openvino==2024.0.0

# Install model optimization tools
pip install openvino-dev==2024.0.0

# Verify installation
python -c "from openvino.runtime import Core; print('OpenVINO OK')"
```

**Option B: Download from Intel**
```bash
# Visit: https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/download.html
# Follow installation instructions for your OS
```

**Requirements**:
- Python 3.8-3.11
- Intel CPU (or compatible processor)
- 2GB free disk space

---

### 🔧 Step 2: Implement Real OpenVINO Adapter

**Replace** `src/aiwork/integrations/openvino_adapter.py` with:

```python
"""
OpenVINO Adapter for AI model optimization and inference.
Provides hardware-accelerated inference on Intel CPUs, GPUs, and VPUs.
"""

import logging
from typing import Dict, Any, Optional, List
import numpy as np

try:
    from openvino.runtime import Core, CompiledModel, InferRequest
    OPENVINO_AVAILABLE = True
except ImportError:
    OPENVINO_AVAILABLE = False
    logging.warning("OpenVINO not available. Install with: pip install openvino")

logger = logging.getLogger(__name__)


class OpenVINOAdapter:
    """
    Production-ready OpenVINO adapter for model optimization and inference.
    
    Example:
        >>> adapter = OpenVINOAdapter()
        >>> compiled = adapter.load_model("model.xml", device="CPU")
        >>> result = adapter.infer(compiled, {"input": np.array([1, 2, 3])})
    """
    
    def __init__(self):
        """Initialize OpenVINO Core."""
        if not OPENVINO_AVAILABLE:
            raise ImportError(
                "OpenVINO is not installed. Install with: pip install openvino"
            )
        
        self.core = Core()
        self.available_devices = self.core.available_devices
        logger.info(f"OpenVINO initialized. Available devices: {self.available_devices}")
    
    def load_model(
        self, 
        model_path: str, 
        device: str = "CPU",
        config: Optional[Dict[str, Any]] = None
    ) -> CompiledModel:
        """
        Load and compile a model for inference.
        
        Args:
            model_path: Path to .xml model file (IR format)
            device: Target device (CPU, GPU, MYRIAD, etc.)
            config: Device-specific configuration
            
        Returns:
            CompiledModel ready for inference
            
        Example:
            >>> model = adapter.load_model("resnet50.xml", device="CPU")
        """
        if device not in self.available_devices:
            logger.warning(
                f"Device {device} not available. Available: {self.available_devices}. "
                f"Falling back to CPU."
            )
            device = "CPU"
        
        logger.info(f"Loading model from {model_path} for device {device}")
        
        # Read model
        model = self.core.read_model(model=model_path)
        
        # Apply configuration
        if config is None:
            config = self._get_default_config(device)
        
        # Compile model
        compiled_model = self.core.compile_model(
            model=model,
            device_name=device,
            config=config
        )
        
        logger.info(
            f"Model compiled successfully. "
            f"Inputs: {[inp.any_name for inp in compiled_model.inputs]}, "
            f"Outputs: {[out.any_name for out in compiled_model.outputs]}"
        )
        
        return compiled_model
    
    def infer(
        self, 
        compiled_model: CompiledModel, 
        inputs: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """
        Run inference on compiled model.
        
        Args:
            compiled_model: Model compiled with load_model()
            inputs: Dictionary mapping input names to numpy arrays
            
        Returns:
            Dictionary mapping output names to numpy arrays
            
        Example:
            >>> result = adapter.infer(model, {"input": np.random.rand(1, 3, 224, 224)})
            >>> print(result["output"])
        """
        # Create inference request
        infer_request = compiled_model.create_infer_request()
        
        # Set inputs
        for input_name, input_data in inputs.items():
            infer_request.set_tensor(input_name, input_data)
        
        # Run inference
        infer_request.infer()
        
        # Get outputs
        outputs = {}
        for output in compiled_model.outputs:
            output_tensor = infer_request.get_tensor(output)
            outputs[output.any_name] = output_tensor.data
        
        return outputs
    
    def optimize_model(
        self,
        model_path: str,
        output_path: str,
        precision: str = "FP16",
        dataset_path: Optional[str] = None
    ) -> str:
        """
        Optimize model using Model Optimizer.
        
        Args:
            model_path: Path to original model (PyTorch, TensorFlow, ONNX)
            output_path: Path to save optimized IR model
            precision: Target precision (FP32, FP16, INT8)
            dataset_path: Path to calibration dataset (for INT8)
            
        Returns:
            Path to optimized model (.xml file)
            
        Note:
            For INT8 quantization, dataset_path is required.
            Use openvino.tools.pot for Post-Training Optimization.
        """
        # This is a simplified example. Real implementation would use:
        # - Model Optimizer (mo) for conversion
        # - Post-Training Optimization Tool (POT) for INT8
        logger.info(
            f"Optimizing model {model_path} to {precision} precision at {output_path}"
        )
        
        # Example command (would be executed via subprocess):
        # mo --input_model {model_path} --output_dir {output_path} --data_type {precision}
        
        raise NotImplementedError(
            "Model optimization requires openvino-dev. "
            "Install with: pip install openvino-dev\n"
            "Then use: mo --input_model model.pt --output_dir output/"
        )
    
    def get_performance_hints(self, device: str) -> Dict[str, Any]:
        """
        Get recommended performance settings for device.
        
        Args:
            device: Target device (CPU, GPU, etc.)
            
        Returns:
            Dictionary of recommended config settings
        """
        hints = {
            "CPU": {
                "PERFORMANCE_HINT": "THROUGHPUT",
                "INFERENCE_PRECISION_HINT": "f32",
                "NUM_STREAMS": "AUTO"
            },
            "GPU": {
                "PERFORMANCE_HINT": "LATENCY",
                "INFERENCE_PRECISION_HINT": "f16",
                "GPU_THROUGHPUT_STREAMS": "AUTO"
            },
            "MYRIAD": {
                "PERFORMANCE_HINT": "THROUGHPUT",
                "VPU_MYRIAD_PROTOCOL": "USB"
            }
        }
        return hints.get(device, hints["CPU"])
    
    def benchmark_model(
        self,
        compiled_model: CompiledModel,
        sample_input: Dict[str, np.ndarray],
        iterations: int = 100
    ) -> Dict[str, float]:
        """
        Benchmark model inference performance.
        
        Args:
            compiled_model: Compiled model
            sample_input: Sample input for inference
            iterations: Number of iterations for benchmarking
            
        Returns:
            Performance metrics (avg_time, throughput, etc.)
        """
        import time
        
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            self.infer(compiled_model, sample_input)
            end = time.perf_counter()
            times.append(end - start)
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        throughput = 1.0 / avg_time
        
        return {
            "avg_inference_time_ms": avg_time * 1000,
            "std_inference_time_ms": std_time * 1000,
            "throughput_fps": throughput,
            "p50_ms": np.percentile(times, 50) * 1000,
            "p95_ms": np.percentile(times, 95) * 1000,
            "p99_ms": np.percentile(times, 99) * 1000,
        }
    
    def _get_default_config(self, device: str) -> Dict[str, Any]:
        """Get default configuration for device."""
        return self.get_performance_hints(device)


# Backward compatibility with stub
def get_openvino_adapter():
    """Factory function for creating OpenVINO adapter."""
    return OpenVINOAdapter()
```

---

### 🔧 Step 3: Update Agent Integration

**Update agent code** to use real OpenVINO:

```python
from aiwork.integrations.openvino_adapter import OpenVINOAdapter
import numpy as np

# Initialize adapter
openvino = OpenVINOAdapter()

# Load optimized model
model = openvino.load_model(
    model_path="models/classifier.xml",
    device="CPU"
)

# Define agent tool
def classify_image(image_path: str) -> dict:
    """Classify image using OpenVINO-optimized model."""
    # Preprocess image
    image = preprocess_image(image_path)  # Your preprocessing
    
    # Run inference
    result = openvino.infer(model, {"input": image})
    
    # Postprocess
    class_id = np.argmax(result["output"])
    confidence = result["output"][0][class_id]
    
    return {
        "class": CLASSES[class_id],
        "confidence": float(confidence)
    }

# Use in agent
agent = Agent(
    role="Image Classifier",
    tools=[classify_image],
    ...
)
```

---

### 🔧 Step 4: Test OpenVINO Integration

**Create test script** (`tests/test_openvino_real.py`):

```python
import pytest
import numpy as np
from aiwork.integrations.openvino_adapter import OpenVINOAdapter

def test_openvino_initialization():
    """Test OpenVINO adapter initializes correctly."""
    adapter = OpenVINOAdapter()
    assert adapter.core is not None
    assert len(adapter.available_devices) > 0

@pytest.mark.skipif(not model_exists(), reason="Test model not available")
def test_model_loading():
    """Test model loading and compilation."""
    adapter = OpenVINOAdapter()
    model = adapter.load_model("tests/fixtures/test_model.xml", device="CPU")
    assert model is not None

@pytest.mark.skipif(not model_exists(), reason="Test model not available")
def test_inference():
    """Test inference execution."""
    adapter = OpenVINOAdapter()
    model = adapter.load_model("tests/fixtures/test_model.xml")
    
    # Create dummy input
    input_shape = model.inputs[0].shape
    dummy_input = {model.inputs[0].any_name: np.random.rand(*input_shape)}
    
    # Run inference
    result = adapter.infer(model, dummy_input)
    
    assert len(result) > 0
    assert all(isinstance(v, np.ndarray) for v in result.values())
```

---

### 📊 Step 5: Benchmark Real Performance

```python
# benchmark_openvino.py
from aiwork.integrations.openvino_adapter import OpenVINOAdapter
import numpy as np

def benchmark():
    adapter = OpenVINOAdapter()
    
    # Load model
    model = adapter.load_model("models/resnet50.xml", device="CPU")
    
    # Create sample input
    sample_input = {
        "input": np.random.rand(1, 3, 224, 224).astype(np.float32)
    }
    
    # Run benchmark
    results = adapter.benchmark_model(model, sample_input, iterations=100)
    
    print("OpenVINO Performance Benchmark")
    print(f"Average Inference Time: {results['avg_inference_time_ms']:.2f}ms")
    print(f"Throughput: {results['throughput_fps']:.2f} FPS")
    print(f"P95 Latency: {results['p95_ms']:.2f}ms")

if __name__ == "__main__":
    benchmark()
```

---

### ✅ Verification Checklist

- [ ] OpenVINO installed and verified
- [ ] Adapter code replaced with production implementation
- [ ] Tests passing with real models
- [ ] Benchmarks show expected performance improvement
- [ ] Documentation updated with real performance numbers
- [ ] Error handling tested (missing models, wrong inputs)
- [ ] Multiple device types tested (CPU, GPU if available)

---

## 2. Kafka Migration

### 📖 Understanding the Current Stub

**Current Implementation** (`src/aiwork/integrations/kafka_adapter.py`):
```python
class KafkaAdapter:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        print(f"Initialized Kafka Adapter connecting to {bootstrap_servers}")

    def produce_task(self, topic: str, task_payload: dict):
        print(f"[Kafka] Producing task to topic '{topic}': {task_payload}")

    def consume_tasks(self, topic: str):
        mock_tasks = [
            {"task_id": "1", "name": "mock_task_1", "params": {}},
            {"task_id": "2", "name": "mock_task_2", "params": {}}
        ]
        for t in mock_tasks:
            yield t
```

**What's Missing**:
- Real Kafka producer/consumer
- Message serialization/deserialization
- Error handling and retries
- Consumer groups and offset management
- Connection health checks

---

### 🔧 Step 1: Install Kafka Client

```bash
# Install confluent-kafka Python client
pip install confluent-kafka==2.3.0

# Verify installation
python -c "from confluent_kafka import Producer, Consumer; print('Kafka client OK')"
```

---

### 🔧 Step 2: Setup Kafka Infrastructure

**Option A: Docker Compose (Recommended for Development)**

Create `docker-compose.kafka.yml`:
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,PLAINTEXT_HOST://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
```

**Start Kafka**:
```bash
docker-compose -f docker-compose.kafka.yml up -d
```

**Option B: Managed Kafka**
- Confluent Cloud
- AWS MSK
- Azure Event Hubs (Kafka-compatible)

---

### 🔧 Step 3: Implement Real Kafka Adapter

**Replace** `src/aiwork/integrations/kafka_adapter.py` with:

```python
"""
Apache Kafka adapter for distributed task processing.
Provides reliable message production and consumption with error handling.
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, Generator
import time

try:
    from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
    from confluent_kafka.admin import AdminClient, NewTopic
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logging.warning("Kafka client not available. Install with: pip install confluent-kafka")

logger = logging.getLogger(__name__)


class KafkaAdapter:
    """
    Production-ready Kafka adapter for distributed task processing.
    
    Example:
        >>> adapter = KafkaAdapter(bootstrap_servers="localhost:9092")
        >>> adapter.produce_task("tasks", {"task_id": "123", "action": "process"})
        >>> for task in adapter.consume_tasks("tasks", group_id="workers"):
        ...     process(task)
    """
    
    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        client_id: str = "aiwork",
        **kwargs
    ):
        """
        Initialize Kafka adapter.
        
        Args:
            bootstrap_servers: Comma-separated list of broker addresses
            client_id: Client identifier for logging
            **kwargs: Additional Kafka configuration
        """
        if not KAFKA_AVAILABLE:
            raise ImportError(
                "confluent-kafka is not installed. "
                "Install with: pip install confluent-kafka"
            )
        
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': client_id,
            **kwargs
        }
        
        logger.info(f"Kafka adapter initialized for {bootstrap_servers}")
    
    def create_producer(self, **config) -> Producer:
        """
        Create Kafka producer with configuration.
        
        Args:
            **config: Additional producer configuration
            
        Returns:
            Configured Producer instance
        """
        producer_config = {
            **self.config,
            'acks': 'all',  # Wait for all replicas
            'retries': 3,
            'max.in.flight.requests.per.connection': 5,
            'compression.type': 'snappy',
            **config
        }
        
        return Producer(producer_config)
    
    def create_consumer(
        self,
        group_id: str,
        topics: list,
        **config
    ) -> Consumer:
        """
        Create Kafka consumer with configuration.
        
        Args:
            group_id: Consumer group ID
            topics: List of topics to subscribe to
            **config: Additional consumer configuration
            
        Returns:
            Configured Consumer instance
        """
        consumer_config = {
            **self.config,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,  # Manual commit for reliability
            'max.poll.interval.ms': 300000,  # 5 minutes
            **config
        }
        
        consumer = Consumer(consumer_config)
        consumer.subscribe(topics)
        
        logger.info(f"Consumer created for group '{group_id}', topics: {topics}")
        
        return consumer
    
    def produce_task(
        self,
        topic: str,
        task_payload: Dict[str, Any],
        key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Produce a task message to Kafka topic.
        
        Args:
            topic: Topic name
            task_payload: Task data (will be JSON serialized)
            key: Optional partition key
            headers: Optional message headers
            
        Raises:
            KafkaException: If message delivery fails
        """
        producer = self.create_producer()
        
        def delivery_callback(err, msg):
            if err:
                logger.error(f"Message delivery failed: {err}")
                raise KafkaException(err)
            else:
                logger.debug(
                    f"Message delivered to {msg.topic()} "
                    f"[partition {msg.partition()}] at offset {msg.offset()}"
                )
        
        # Serialize payload
        value = json.dumps(task_payload).encode('utf-8')
        key_bytes = key.encode('utf-8') if key else None
        
        # Convert headers
        kafka_headers = []
        if headers:
            kafka_headers = [(k, v.encode('utf-8')) for k, v in headers.items()]
        
        # Produce message
        producer.produce(
            topic=topic,
            value=value,
            key=key_bytes,
            headers=kafka_headers,
            callback=delivery_callback
        )
        
        # Wait for delivery
        producer.flush(timeout=10)
        
        logger.info(f"Task produced to topic '{topic}': {task_payload.get('task_id', 'unknown')}")
    
    def consume_tasks(
        self,
        topic: str,
        group_id: str = "aiwork-workers",
        handler: Optional[Callable] = None,
        max_messages: Optional[int] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Consume tasks from Kafka topic.
        
        Args:
            topic: Topic name
            group_id: Consumer group ID
            handler: Optional callback function for processing
            max_messages: Optional limit on number of messages to consume
            
        Yields:
            Deserialized task payloads
            
        Example:
            >>> def process_task(task):
            ...     print(f"Processing {task['task_id']}")
            ...     return {"status": "success"}
            >>> 
            >>> for task in adapter.consume_tasks("tasks", handler=process_task):
            ...     print(f"Completed: {task}")
        """
        consumer = self.create_consumer(group_id=group_id, topics=[topic])
        
        messages_consumed = 0
        
        try:
            while True:
                # Check max_messages limit
                if max_messages and messages_consumed >= max_messages:
                    break
                
                # Poll for messages
                msg = consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(f"Reached end of partition {msg.partition()}")
                        continue
                    else:
                        raise KafkaException(msg.error())
                
                # Deserialize message
                try:
                    task = json.loads(msg.value().decode('utf-8'))
                    messages_consumed += 1
                    
                    logger.info(f"Consumed task: {task.get('task_id', 'unknown')}")
                    
                    # Call handler if provided
                    if handler:
                        try:
                            result = handler(task)
                            task['_handler_result'] = result
                        except Exception as e:
                            logger.error(f"Handler failed for task {task}: {e}")
                            task['_handler_error'] = str(e)
                    
                    # Commit offset
                    consumer.commit(message=msg)
                    
                    yield task
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to deserialize message: {e}")
                    consumer.commit(message=msg)  # Commit to skip bad message
                    continue
                
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        finally:
            consumer.close()
            logger.info("Consumer closed")
    
    def create_topic(
        self,
        topic: str,
        num_partitions: int = 3,
        replication_factor: int = 1
    ) -> None:
        """
        Create a Kafka topic.
        
        Args:
            topic: Topic name
            num_partitions: Number of partitions
            replication_factor: Replication factor
        """
        admin_client = AdminClient({'bootstrap.servers': self.bootstrap_servers})
        
        new_topic = NewTopic(
            topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        
        fs = admin_client.create_topics([new_topic])
        
        for topic, f in fs.items():
            try:
                f.result()
                logger.info(f"Topic '{topic}' created successfully")
            except Exception as e:
                logger.error(f"Failed to create topic '{topic}': {e}")
    
    def check_health(self) -> bool:
        """
        Check Kafka cluster health.
        
        Returns:
            True if cluster is reachable, False otherwise
        """
        try:
            admin_client = AdminClient({'bootstrap.servers': self.bootstrap_servers})
            metadata = admin_client.list_topics(timeout=5)
            logger.info(f"Kafka cluster healthy. Brokers: {len(metadata.brokers)}")
            return True
        except Exception as e:
            logger.error(f"Kafka cluster unreachable: {e}")
            return False


# Factory function
def get_kafka_adapter(bootstrap_servers: str = "localhost:9092") -> KafkaAdapter:
    """Create Kafka adapter instance."""
    return KafkaAdapter(bootstrap_servers=bootstrap_servers)
```

---

### 🔧 Step 4: Update Application to Use Kafka

**Distributed Worker Pattern**:

```python
# worker.py - Runs on multiple machines
from aiwork.integrations.kafka_adapter import KafkaAdapter
from aiwork.orchestrator import Orchestrator

def process_task(task_data):
    """Process individual task."""
    # Create flow from task
    flow = create_flow_from_task(task_data)
    
    # Execute
    orch = Orchestrator()
    result = orch.execute(flow, task_data.get('context', {}))
    
    return result

def main():
    kafka = KafkaAdapter(bootstrap_servers="kafka:9092")
    
    # Consume and process tasks
    for task in kafka.consume_tasks(
        topic="aiwork-tasks",
        group_id="aiwork-workers",
        handler=process_task
    ):
        print(f"Completed task: {task['task_id']}")

if __name__ == "__main__":
    main()
```

**Producer (API Server)**:

```python
# api_server.py
from fastapi import FastAPI
from aiwork.integrations.kafka_adapter import KafkaAdapter

app = FastAPI()
kafka = KafkaAdapter(bootstrap_servers="kafka:9092")

@app.post("/execute-async")
async def execute_async(flow_definition: dict):
    """Submit task to Kafka for async processing."""
    task_id = str(uuid.uuid4())
    
    kafka.produce_task(
        topic="aiwork-tasks",
        task_payload={
            "task_id": task_id,
            "flow": flow_definition,
            "timestamp": time.time()
        }
    )
    
    return {"task_id": task_id, "status": "queued"}
```

---

### 🔧 Step 5: Test Kafka Integration

```python
# tests/test_kafka_real.py
import pytest
from aiwork.integrations.kafka_adapter import KafkaAdapter

@pytest.fixture
def kafka():
    return KafkaAdapter(bootstrap_servers="localhost:9093")

def test_produce_and_consume(kafka):
    """Test round-trip message flow."""
    topic = "test-topic"
    test_task = {"task_id": "test-123", "action": "process"}
    
    # Produce
    kafka.produce_task(topic, test_task)
    
    # Consume
    consumed = []
    for task in kafka.consume_tasks(topic, group_id="test-group", max_messages=1):
        consumed.append(task)
    
    assert len(consumed) == 1
    assert consumed[0]["task_id"] == "test-123"

def test_health_check(kafka):
    """Test Kafka cluster health check."""
    assert kafka.check_health() is True
```

---

### ✅ Verification Checklist

- [ ] Kafka cluster running (docker-compose or managed)
- [ ] confluent-kafka installed
- [ ] Producer sends messages successfully
- [ ] Consumer receives and processes messages
- [ ] Consumer group management working
- [ ] Error handling tested (broker down, bad messages)
- [ ] Performance tested (throughput, latency)
- [ ] Multiple workers tested (distributed processing)

---

## 3. Redis Migration

### 📖 Understanding the Current Partial Implementation

**Current Implementation** (`src/aiwork/memory/state_manager.py`):
```python
class StateManager:
    def __init__(self, use_redis=False):
        self.use_redis = use_redis
        self.local_store = {}  # Works
        if use_redis:
            print("Initializing Redis connection...")
            # self.redis = redis.Redis(...)  # Not implemented

    def save_state(self, flow_id: str, state: dict):
        if self.use_redis:
            pass  # Would save to Redis
        else:
            self.local_store[flow_id] = state  # Works

    def get_state(self, flow_id: str):
        if self.use_redis:
            return {}  # Would retrieve from Redis
        return self.local_store.get(flow_id, {})  # Works
```

---

### 🔧 Step 1: Install Redis

**Option A: Docker (Recommended)**
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine \
  redis-server --appendonly yes
```

**Option B: System Package**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

**Install Python Client**:
```bash
pip install redis==5.0.1
```

---

### 🔧 Step 2: Implement Full Redis Support

**Replace** `src/aiwork/memory/state_manager.py` with:

```python
"""
State management with Redis support for distributed deployments.
"""

import json
import logging
from typing import Dict, Any, Optional
import pickle

try:
    import redis
    from redis.connection import ConnectionPool
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis not available. Install with: pip install redis")

logger = logging.getLogger(__name__)


class StateManager:
    """
    Manage workflow state with local or Redis storage.
    
    Example:
        >>> # Local storage
        >>> state = StateManager(use_redis=False)
        >>> state.save_state("flow-1", {"step": 1, "data": "..."})
        
        >>> # Redis storage (distributed)
        >>> state = StateManager(use_redis=True, redis_url="redis://localhost:6379")
        >>> state.save_state("flow-1", {"step": 1, "data": "..."})
    """
    
    def __init__(
        self,
        use_redis: bool = False,
        redis_url: str = "redis://localhost:6379",
        redis_db: int = 0,
        ttl_seconds: Optional[int] = None,
        **redis_kwargs
    ):
        """
        Initialize state manager.
        
        Args:
            use_redis: Use Redis for distributed state
            redis_url: Redis connection URL
            redis_db: Redis database number
            ttl_seconds: Optional TTL for state entries (seconds)
            **redis_kwargs: Additional Redis connection parameters
        """
        self.use_redis = use_redis
        self.local_store = {}
        self.ttl_seconds = ttl_seconds
        
        if use_redis:
            if not REDIS_AVAILABLE:
                raise ImportError(
                    "Redis is not installed. Install with: pip install redis"
                )
            
            # Create connection pool
            self.pool = ConnectionPool.from_url(
                redis_url,
                db=redis_db,
                decode_responses=False,  # Handle binary data
                max_connections=10,
                **redis_kwargs
            )
            
            self.redis = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            try:
                self.redis.ping()
                logger.info(f"Redis connected successfully to {redis_url}")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        else:
            self.redis = None
            logger.info("Using local in-memory state storage")
    
    def save_state(self, flow_id: str, state: Dict[str, Any]) -> None:
        """
        Save workflow state.
        
        Args:
            flow_id: Unique workflow identifier
            state: State dictionary to save
        """
        if self.use_redis:
            # Serialize with pickle for full Python object support
            serialized = pickle.dumps(state)
            
            if self.ttl_seconds:
                self.redis.setex(
                    name=f"state:{flow_id}",
                    time=self.ttl_seconds,
                    value=serialized
                )
            else:
                self.redis.set(f"state:{flow_id}", serialized)
            
            logger.debug(f"State saved to Redis for flow '{flow_id}'")
        else:
            self.local_store[flow_id] = state
            logger.debug(f"State saved locally for flow '{flow_id}'")
    
    def get_state(self, flow_id: str) -> Dict[str, Any]:
        """
        Retrieve workflow state.
        
        Args:
            flow_id: Unique workflow identifier
            
        Returns:
            State dictionary or empty dict if not found
        """
        if self.use_redis:
            serialized = self.redis.get(f"state:{flow_id}")
            if serialized:
                state = pickle.loads(serialized)
                logger.debug(f"State retrieved from Redis for flow '{flow_id}'")
                return state
            else:
                logger.debug(f"No state found in Redis for flow '{flow_id}'")
                return {}
        else:
            state = self.local_store.get(flow_id, {})
            logger.debug(f"State retrieved locally for flow '{flow_id}'")
            return state
    
    def delete_state(self, flow_id: str) -> None:
        """
        Delete workflow state.
        
        Args:
            flow_id: Unique workflow identifier
        """
        if self.use_redis:
            self.redis.delete(f"state:{flow_id}")
            logger.debug(f"State deleted from Redis for flow '{flow_id}'")
        else:
            self.local_store.pop(flow_id, None)
            logger.debug(f"State deleted locally for flow '{flow_id}'")
    
    def list_flows(self) -> list:
        """
        List all stored flow IDs.
        
        Returns:
            List of flow IDs
        """
        if self.use_redis:
            keys = self.redis.keys("state:*")
            return [key.decode('utf-8').replace("state:", "") for key in keys]
        else:
            return list(self.local_store.keys())
    
    def clear_all(self) -> None:
        """Clear all state data. Use with caution!"""
        if self.use_redis:
            keys = self.redis.keys("state:*")
            if keys:
                self.redis.delete(*keys)
            logger.warning("All Redis state data cleared")
        else:
            self.local_store.clear()
            logger.warning("All local state data cleared")
    
    def check_health(self) -> bool:
        """
        Check Redis connection health.
        
        Returns:
            True if healthy, False otherwise
        """
        if self.use_redis:
            try:
                self.redis.ping()
                return True
            except redis.ConnectionError:
                return False
        return True  # Local storage always healthy


# Factory functions
def get_local_state_manager() -> StateManager:
    """Create local state manager."""
    return StateManager(use_redis=False)


def get_redis_state_manager(
    redis_url: str = "redis://localhost:6379",
    **kwargs
) -> StateManager:
    """Create Redis-backed state manager."""
    return StateManager(use_redis=True, redis_url=redis_url, **kwargs)
```

---

### 🔧 Step 3: Update Configuration

**Create** `config/production.py`:
```python
# Production configuration
import os

REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
STATE_TTL_SECONDS = int(os.getenv("STATE_TTL_SECONDS", "86400"))  # 24 hours

def get_state_manager():
    from aiwork.memory.state_manager import StateManager
    return StateManager(
        use_redis=REDIS_ENABLED,
        redis_url=REDIS_URL,
        redis_db=REDIS_DB,
        ttl_seconds=STATE_TTL_SECONDS
    )
```

---

### 🔧 Step 4: Test Redis Integration

```python
# tests/test_redis_real.py
import pytest
from aiwork.memory.state_manager import StateManager

@pytest.fixture
def redis_state():
    return StateManager(use_redis=True, redis_url="redis://localhost:6379")

def test_save_and_retrieve(redis_state):
    """Test state save and retrieval."""
    flow_id = "test-flow-1"
    state = {"step": 1, "data": "test"}
    
    redis_state.save_state(flow_id, state)
    retrieved = redis_state.get_state(flow_id)
    
    assert retrieved == state
    
    # Cleanup
    redis_state.delete_state(flow_id)

def test_ttl(redis_state):
    """Test state expiration."""
    state = StateManager(
        use_redis=True,
        redis_url="redis://localhost:6379",
        ttl_seconds=1
    )
    
    state.save_state("temp-flow", {"data": "temp"})
    
    import time
    time.sleep(2)
    
    retrieved = state.get_state("temp-flow")
    assert retrieved == {}  # Should be expired

def test_health_check(redis_state):
    """Test Redis health check."""
    assert redis_state.check_health() is True
```

---

### ✅ Verification Checklist

- [ ] Redis server running
- [ ] redis-py installed
- [ ] State saves to Redis successfully
- [ ] State retrieves from Redis successfully
- [ ] TTL working (if configured)
- [ ] Multiple processes can share state
- [ ] Error handling tested (Redis down, connection errors)
- [ ] Migration from local to Redis tested

---

## 4. Docker Deployment

### 🐳 Complete Docker Setup

**Create** `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Redis for distributed state
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Kafka + Zookeeper for distributed processing
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    healthcheck:
      test: ["CMD", "echo", "ruok", "|", "nc", "localhost", "2181"]
      interval: 10s
      timeout: 3s
      retries: 3

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions", "--bootstrap-server", "localhost:9092"]
      interval: 10s
      timeout: 3s
      retries: 3

  # AIWork API Server
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - REDIS_ENABLED=true
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - redis
      - kafka
    command: uvicorn aiwork.api.server:app --host 0.0.0.0 --port 8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  # AIWork Worker (scales horizontally)
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - REDIS_ENABLED=true
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - redis
      - kafka
    command: python -m aiwork.worker
    deploy:
      replicas: 3  # Run 3 workers

volumes:
  redis-data:

networks:
  default:
    name: aiwork-network
```

**Create** `Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install AIWork
RUN pip install -e .

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "aiwork.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy**:
```bash
# Build and start all services
docker-compose up -d

# Scale workers
docker-compose up -d --scale worker=5

# Check logs
docker-compose logs -f api worker

# Stop all
docker-compose down
```

---

## 5. Performance Tuning

### 🎯 OpenVINO Optimization

```python
# Optimize for throughput
config = {
    "PERFORMANCE_HINT": "THROUGHPUT",
    "NUM_STREAMS": "AUTO",
    "INFERENCE_NUM_THREADS": 4
}
model = openvino.load_model("model.xml", device="CPU", config=config)

# Optimize for latency
config = {
    "PERFORMANCE_HINT": "LATENCY",
    "NUM_STREAMS": 1
}
model = openvino.load_model("model.xml", device="CPU", config=config)
```

### ⚡ Kafka Optimization

```python
# Producer: Batch messages
producer_config = {
    'batch.size': 32768,  # 32KB
    'linger.ms': 10,  # Wait 10ms for batching
    'compression.type': 'snappy'
}

# Consumer: Prefetch messages
consumer_config = {
    'fetch.min.bytes': 1024,
    'fetch.wait.max.ms': 500,
    'max.partition.fetch.bytes': 1048576  # 1MB
}
```

### 💾 Redis Optimization

```python
# Use pipelining for batch operations
pipe = redis.pipeline()
for i in range(100):
    pipe.set(f"key:{i}", f"value:{i}")
pipe.execute()

# Use connection pooling
pool = ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=False
)
```

---

## 6. Production Configuration

### Environment Variables

Create `.env.production`:
```bash
# Application
APP_ENV=production
LOG_LEVEL=INFO
WORKER_COUNT=4

# Redis
REDIS_ENABLED=true
REDIS_URL=redis://redis-cluster:6379
REDIS_DB=0
REDIS_PASSWORD=your-secure-password
STATE_TTL_SECONDS=86400

# Kafka
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=kafka-1:9092,kafka-2:9092,kafka-3:9092
KAFKA_CONSUMER_GROUP=aiwork-workers
KAFKA_AUTO_COMMIT=false

# OpenVINO
OPENVINO_DEVICE=CPU
OPENVINO_PRECISION=FP16
OPENVINO_NUM_STREAMS=AUTO

# Security
API_KEY_ENABLED=true
API_KEY=your-secure-api-key
CORS_ORIGINS=https://yourdomain.com

# Monitoring
METRICS_ENABLED=true
METRICS_PORT=9090
TRACING_ENABLED=true
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
```

---

## 7. Troubleshooting

### OpenVINO Issues

**Problem**: "Device not found"
```python
# Solution: Check available devices
adapter = OpenVINOAdapter()
print(adapter.available_devices)
# Use available device
model = adapter.load_model("model.xml", device="CPU")
```

**Problem**: "Model format not supported"
```bash
# Solution: Convert model with Model Optimizer
mo --input_model model.onnx --output_dir ./optimized/
```

### Kafka Issues

**Problem**: "Broker not available"
```python
# Solution: Check health
kafka = KafkaAdapter(bootstrap_servers="localhost:9092")
if not kafka.check_health():
    print("Kafka cluster unreachable")
```

**Problem**: "Consumer lag"
```bash
# Solution: Scale workers
docker-compose up -d --scale worker=10
```

### Redis Issues

**Problem**: "Connection refused"
```bash
# Solution: Check Redis is running
docker ps | grep redis
redis-cli ping
```

**Problem**: "Out of memory"
```bash
# Solution: Configure Redis maxmemory
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## Summary

This guide provides complete, step-by-step instructions for migrating AIWork from stub implementations to production-ready integrations. Follow these steps to:

✅ Implement real OpenVINO integration for hardware acceleration  
✅ Deploy distributed processing with Kafka  
✅ Enable shared state with Redis  
✅ Deploy with Docker for scalability  
✅ Optimize performance for production workloads  
✅ Configure for security and reliability  

**Questions?** See [MOCK_IMPLEMENTATIONS.md](MOCK_IMPLEMENTATIONS.md) or open a GitHub issue.

---

<div align="center">
  <sub>Built with ❤️ for production deployments</sub>
</div>
