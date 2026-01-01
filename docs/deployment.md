# 🚀 AIWork Deployment Guide

Complete guide for deploying AIWork in development, production, and cloud environments.

---

## Table of Contents

1. [Local Development](#1-local-development)
2. [Production Deployment](#2-production-deployment)
3. [Intel® DevCloud Deployment](#3-intel-devcloud-deployment)
4. [Docker Deployment](#4-docker-deployment)
5. [Monitoring & Observability](#5-monitoring--observability)
6. [Security & Best Practices](#6-security--best-practices)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Local Development

The simplest way to run AIWork on your local machine for development and testing.

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository
- **Virtual Environment**: Recommended for isolation

### Installation Steps

#### Step 1: Clone the Repository

```bash
git clone https://github.com/JayeshCC/Aiwork.git
cd Aiwork
```

#### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Step 3: Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Verify Installation

```bash
# Run quickstart example
python examples/quickstart.py
```

**Expected Output:**
```
Starting Flow: document_pipeline
  Executing Task: extract...
    [Logic] Extracting text from document...
  Task extract Completed.
  Executing Task: summarize...
    [Logic] Summarizing text: 'Sample document content from Intel AI Challenge'
  Task summarize Completed.
Flow document_pipeline Finished.

Final Output:
{'extract': {'text': 'Sample document content from Intel AI Challenge'}, 
 'summarize': {'summary': 'Sample document conte...'}}
```

### Running Examples

**Document Processor Agent:**
```bash
python examples/agents/document_processor/run.py
```

**Customer Support Agent:**
```bash
python examples/agents/customer_support/run.py
```

**Memory Demo:**
```bash
python examples/memory_demo.py
```

**Airflow Export Demo:**
```bash
python examples/airflow_export_demo.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=src/aiwork --cov-report=html

# Run verbose
pytest -v
```

### Starting the REST API Server

```bash
# Start server
python -m aiwork.api.server

# Server runs on http://localhost:8000
# Access API docs at http://localhost:8000/docs
```

Test the API:
```bash
curl http://localhost:8000/
```

---

## 2. Production Deployment

Deploy AIWork in production environments with scalability and reliability.

### Architecture Options

#### Option A: Single Server Deployment

```
[Client] → [Load Balancer] → [AIWork Server] → [Redis]
                                              → [PostgreSQL]
```

**Best for:** Small to medium workloads, <100 req/s

#### Option B: Distributed Deployment

```
[Clients] → [API Gateway] → [Load Balancer] → [AIWork Workers (N)]
                                             → [Kafka Cluster]
                                             → [Redis Cluster]
                                             → [PostgreSQL]
```

**Best for:** Large workloads, >1000 req/s, high availability

### Production Setup

#### Step 1: System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB
- OS: Ubuntu 20.04 LTS or later

**Recommended (Intel Hardware):**
- CPU: Intel® Xeon® Scalable Processor (8+ cores)
- RAM: 32GB
- Storage: 100GB SSD
- OS: Ubuntu 22.04 LTS

#### Step 2: Install System Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.9+
sudo apt-get install -y python3.9 python3.9-venv python3-pip

# Install build tools
sudo apt-get install -y build-essential git

# Install Redis (optional)
sudo apt-get install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### Step 3: Deploy Application

```bash
# Create application directory
sudo mkdir -p /opt/aiwork
sudo chown $USER:$USER /opt/aiwork
cd /opt/aiwork

# Clone repository
git clone https://github.com/JayeshCC/Aiwork.git .

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

#### Step 4: Configure Environment

Create `.env` file:

```bash
# .env
ENVIRONMENT=production
LOG_LEVEL=INFO
REDIS_URL=redis://localhost:6379
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
API_HOST=0.0.0.0
API_PORT=8000
WORKERS=4
```

Load environment:
```bash
export $(cat .env | xargs)
```

#### Step 5: Run with Gunicorn

```bash
# Start API server with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info \
  --access-logfile /var/log/aiwork/access.log \
  --error-logfile /var/log/aiwork/error.log \
  aiwork.api.server:app
```

#### Step 6: Setup as System Service

Create systemd service file `/etc/systemd/system/aiwork.service`:

```ini
[Unit]
Description=AIWork API Server
After=network.target redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/aiwork
Environment="PATH=/opt/aiwork/venv/bin"
EnvironmentFile=/opt/aiwork/.env
ExecStart=/opt/aiwork/venv/bin/gunicorn \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  aiwork.api.server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aiwork
sudo systemctl start aiwork
sudo systemctl status aiwork
```

### Production Configuration with Kafka

#### Step 1: Install Kafka

```bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka
bin/kafka-server-start.sh config/server.properties &
```

#### Step 2: Create Topics

```bash
# Create task queue topic
bin/kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic aiwork.tasks

# Create results topic
bin/kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic aiwork.results
```

#### Step 3: Create Worker Service

Create `worker.py`:

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from aiwork.integrations.kafka_adapter import KafkaAdapter
from aiwork.orchestrator import Orchestrator
from aiwork.core.flow import Flow

kafka = KafkaAdapter(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))

print("Worker started, waiting for tasks...")
for task in kafka.consume_tasks("aiwork.tasks"):
    print(f"Processing task: {task['task_id']}")
    
    # Build flow from task definition
    flow = build_flow_from_definition(task)
    
    # Execute
    orch = Orchestrator()
    result = orch.execute(flow, task["context"])
    
    # Send result
    kafka.produce_task("aiwork.results", {
        "task_id": task["task_id"],
        "status": "completed",
        "outputs": result["outputs"]
    })
```

Run multiple workers:
```bash
# Terminal 1
python worker.py

# Terminal 2
python worker.py

# Terminal 3
python worker.py
```

### Production Configuration with Redis

Create `config.py`:

```python
from aiwork.memory.state_manager import StateManager

# Production state manager with Redis
state = StateManager(
    use_redis=True,
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379")
)

# Use in workflows
def execute_with_state(flow, flow_id, context):
    # Save initial state
    state.save_state(flow_id, {
        "status": "started",
        "context": context
    })
    
    # Execute
    orch = Orchestrator()
    result = orch.execute(flow, context)
    
    # Save final state
    state.save_state(flow_id, {
        "status": "completed",
        "result": result
    })
    
    return result
```

### Load Balancer Configuration (Nginx)

Install Nginx:
```bash
sudo apt-get install -y nginx
```

Create `/etc/nginx/sites-available/aiwork`:

```nginx
upstream aiwork_backend {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name aiwork.example.com;

    location / {
        proxy_pass http://aiwork_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://aiwork_backend/;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/aiwork /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 3. Intel® DevCloud Deployment

Deploy and benchmark on Intel® Xeon® processors via Intel DevCloud.

### Prerequisites

- Intel DevCloud account: [devcloud.intel.com](https://devcloud.intel.com)
- SSH client (for terminal access)
- JupyterLab (for interactive development)

### Getting Started

#### Option A: JupyterLab Interface

1. **Log in to DevCloud**
   - Go to [devcloud.intel.com](https://devcloud.intel.com)
   - Sign in with your Intel account

2. **Launch JupyterLab**
   - Click "Launch JupyterLab"
   - Wait for environment to initialize

3. **Upload Code**
   - Use the Upload button to upload AIWork repository
   - Or clone from GitHub:
   ```bash
   git clone https://github.com/JayeshCC/Aiwork.git
   cd Aiwork
   ```

4. **Setup Environment**
   ```bash
   # Create conda environment
   conda create -n aiwork_env python=3.9 -y
   conda activate aiwork_env
   
   # Install dependencies
   pip install -r requirements.txt
   ```

5. **Run Examples**
   ```bash
   python examples/quickstart.py
   python examples/agents/document_processor/run.py
   ```

#### Option B: Batch Job Submission

For longer-running workloads, submit as batch jobs.

**Create job script `run_benchmark.sh`:**

```bash
#!/bin/bash

# Request specific node type
#PBS -l nodes=1:xeon:ppn=4
#PBS -l walltime=01:00:00
#PBS -N aiwork_benchmark

# Change to working directory
cd $PBS_O_WORKDIR

# Activate environment
source activate aiwork_env

# Run benchmark
python benchmarks/openvino_benchmark.py

# Run full workflow
python examples/agents/document_processor/run.py
```

**Submit job:**

```bash
qsub run_benchmark.sh
```

**Check job status:**

```bash
qstat -u $USER
```

**View output:**

```bash
cat aiwork_benchmark.o<job_id>
cat aiwork_benchmark.e<job_id>
```

### DevCloud Node Types

Choose appropriate node for your workload:

| Node Type | CPU | Cores | RAM | Use Case |
|-----------|-----|-------|-----|----------|
| `xeon` | Xeon Scalable | 4-48 | 96-192GB | General compute |
| `xeon:gold` | Xeon Gold | 24-48 | 192GB | High performance |
| `xeon:platinum` | Xeon Platinum | 40-112 | 192-384GB | Benchmarking |

**Example job submissions:**

```bash
# Standard Xeon node
qsub -l nodes=1:xeon:ppn=8 run_benchmark.sh

# High-memory node
qsub -l nodes=1:xeon:gold:ppn=24 run_benchmark.sh

# Platinum node for benchmarks
qsub -l nodes=1:xeon:platinum:ppn=40 run_benchmark.sh
```

### Running Benchmarks on DevCloud

```bash
# Run OpenVINO benchmark
python benchmarks/openvino_benchmark.py > benchmark_results.txt

# Compare results
cat benchmark_results.txt
```

**Expected Output:**
```
=== Intel OpenVINO Benchmark Results ===

Starting benchmark for DistilBERT...
  [DistilBERT] PyTorch/Standard Latency: 45.23 ms
  [DistilBERT] OpenVINO Latency: 12.18 ms
  [DistilBERT] Speedup: 3.71x

Starting benchmark for OCR Model...
  [OCR Model] PyTorch/Standard Latency: 156.45 ms
  [OCR Model] OpenVINO Latency: 42.33 ms
  [OCR Model] Speedup: 3.70x

=== Summary ===
Average Speedup: 3.70x
Optimization: ENABLED (Intel OpenVINO)
```

---

## 4. Docker Deployment

Containerize AIWork for portable, scalable deployment.

### Simple Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY examples/ examples/
COPY benchmarks/ benchmarks/

# Set Python path
ENV PYTHONPATH=/app/src

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "-m", "aiwork.api.server"]
```

### Build and Run

```bash
# Build image
docker build -t aiwork:latest .

# Run container
docker run -p 8000:8000 aiwork:latest

# Run with environment variables
docker run -p 8000:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379 \
  -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
  aiwork:latest
```

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # AIWork API Server
  aiwork-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - redis
      - kafka
    restart: unless-stopped

  # Redis for state management
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

  # Zookeeper for Kafka
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    restart: unless-stopped

  # Kafka for distributed messaging
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
    restart: unless-stopped

  # AIWork Worker (scales independently)
  aiwork-worker:
    build: .
    command: python worker.py
    environment:
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - redis
      - kafka
    deploy:
      replicas: 3
    restart: unless-stopped

volumes:
  redis-data:
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale workers
docker-compose up -d --scale aiwork-worker=5

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Production Docker Image

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git

# Copy and install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 aiwork && \
    chown -R aiwork:aiwork /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=aiwork:aiwork src/ src/
COPY --chown=aiwork:aiwork examples/ examples/

ENV PYTHONPATH=/app/src

# Switch to non-root user
USER aiwork

EXPOSE 8000

CMD ["python", "-m", "aiwork.api.server"]
```

Build production image:
```bash
docker build -f Dockerfile.prod -t aiwork:prod .
```

---

## 5. Monitoring & Observability

### Application Metrics

AIWork collects built-in metrics:

```python
from aiwork.core.observability import metrics

# Get all metrics
all_metrics = metrics.get("task_duration_seconds")

for metric in all_metrics:
    print(f"Task: {metric['tags']['task']}")
    print(f"Duration: {metric['value']:.2f}s")
    print(f"Status: {metric['tags']['status']}")
```

### Prometheus Integration

Create `prometheus_exporter.py`:

```python
from prometheus_client import start_http_server, Gauge, Counter
from aiwork.core.observability import metrics
import time

# Define Prometheus metrics
task_duration = Gauge('aiwork_task_duration_seconds', 
                      'Task execution duration',
                      ['task', 'status'])
task_count = Counter('aiwork_task_total', 
                     'Total tasks executed',
                     ['task', 'status'])

def export_metrics():
    """Export AIWork metrics to Prometheus format"""
    while True:
        # Get metrics from AIWork
        durations = metrics.get("task_duration_seconds")
        
        for metric in durations:
            task_name = metric['tags']['task']
            status = metric['tags']['status']
            duration = metric['value']
            
            # Update Prometheus metrics
            task_duration.labels(task=task_name, status=status).set(duration)
            task_count.labels(task=task_name, status=status).inc()
        
        time.sleep(15)  # Update every 15 seconds

if __name__ == '__main__':
    # Start Prometheus metrics server on port 9090
    start_http_server(9090)
    export_metrics()
```

Run exporter:
```bash
pip install prometheus-client
python prometheus_exporter.py &
```

### Logging Configuration

Create `logging_config.py`:

```python
import logging
import sys

def setup_logging(level=logging.INFO):
    """Configure application logging"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler('aiwork.log')
    file_handler.setFormatter(formatter)
    
    # Root logger
    logger = logging.getLogger('aiwork')
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage
logger = setup_logging()
logger.info("AIWork started")
```

### Health Checks

Add health check endpoint:

```python
# In aiwork.api.server

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "components": {
            "redis": check_redis_connection(),
            "kafka": check_kafka_connection()
        }
    }

def check_redis_connection():
    try:
        # Check Redis
        state = StateManager(use_redis=True)
        state.save_state("health_check", {"test": True})
        return "healthy"
    except:
        return "unhealthy"

def check_kafka_connection():
    try:
        # Check Kafka
        kafka = KafkaAdapter()
        return "healthy"
    except:
        return "unhealthy"
```

---

## 6. Security & Best Practices

### Environment Variables

Never commit secrets. Use environment variables:

```bash
# .env (add to .gitignore)
REDIS_PASSWORD=your_secure_password
KAFKA_SASL_USERNAME=your_username
KAFKA_SASL_PASSWORD=your_password
API_KEY=your_api_key
```

Load in application:
```python
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
```

### API Authentication

Add API key authentication:

```python
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/execute")
def execute_flow(request: FlowRequest, api_key: str = Depends(verify_api_key)):
    # Execute flow
    ...
```

### Rate Limiting

Install slowapi:
```bash
pip install slowapi
```

Add rate limiting:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/execute")
@limiter.limit("10/minute")
def execute_flow(request: Request, flow_request: FlowRequest):
    # Execute flow
    ...
```

---

## 7. Troubleshooting

### Common Issues

#### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m aiwork.api.server --port 8001
```

#### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'aiwork'`

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/Aiwork/src:$PYTHONPATH

# Or install in development mode
pip install -e .
```

#### Redis Connection Failed

**Error:** `redis.exceptions.ConnectionError`

**Solution:**
```bash
# Check Redis is running
redis-cli ping

# Start Redis if not running
sudo systemctl start redis-server

# Or use local state
state = StateManager(use_redis=False)
```

#### Memory Issues

**Error:** `MemoryError` or OOM

**Solution:**
```bash
# Increase available memory
# Reduce batch sizes
# Use streaming for large datasets
# Enable swap

sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Performance Tuning

**Slow API responses:**

1. Enable caching
2. Use Redis for state
3. Optimize task handlers
4. Use OpenVINO for ML models
5. Scale horizontally with workers

**High CPU usage:**

1. Profile with cProfile
2. Optimize bottleneck tasks
3. Use multiprocessing for CPU-bound work
4. Limit concurrent requests

---

## Summary

AIWork supports multiple deployment patterns:

| Pattern | Best For | Complexity | Scalability |
|---------|----------|------------|-------------|
| Local Dev | Development, Testing | Low | N/A |
| Single Server | Small apps, <100 req/s | Low | Vertical |
| Docker | Portability, Consistency | Medium | Horizontal |
| Distributed (Kafka) | High throughput, >1000 req/s | High | Horizontal |
| Intel DevCloud | Benchmarking, R&D | Medium | Platform |

Choose the pattern that fits your requirements and scale as needed!

---

## See Also

- [User Guide](USER_GUIDE.md) - How to use AIWork
- [Architecture](ARCHITECTURE.md) - System design
- [API Reference](API_REFERENCE.md) - API documentation
- [Benchmarks](BENCHMARKS.md) - Performance data

---

<div align="center">
  <sub>Built with ❤️ for the Intel AI Innovation Challenge 2024</sub>
</div>
