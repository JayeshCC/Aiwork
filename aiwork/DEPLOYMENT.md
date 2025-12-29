# 🚀 Deployment Guide for AIWork

This guide covers how to deploy the **AIWork** framework in different environments.

## 1. Local Deployment (Development)

The simplest way to run AIWork is on your local machine.

### Prerequisites
*   Python 3.8+
*   `pip` (Python Package Manager)

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/JayeshCC/aiwork.git
    cd aiwork
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run a Reference Agent:**
    ```bash
    python examples/agents/document_processor/run.py
    ```

---

## 2. Intel® DevCloud Deployment

To benchmark and run on Intel® Xeon® Scalable Processors.

### Steps
1.  **Log in to DevCloud:**
    Access the JupyterHub interface at [devcloud.intel.com](https://devcloud.intel.com).

2.  **Upload Code:**
    Upload the `aiwork` folder to your DevCloud workspace.

3.  **Open a Terminal in JupyterHub:**
    Run the following commands:

    ```bash
    cd aiwork
    
    # Create a dedicated environment
    conda create -n aiwork_env python=3.9
    conda activate aiwork_env
    
    # Install dependencies (Intel optimized versions are often pre-installed, but this ensures compatibility)
    pip install -r requirements.txt
    ```

4.  **Submit a Job (Batch Mode):**
    Create a script `job.sh`:
    ```bash
    #!/bin/bash
    source activate aiwork_env
    python examples/agents/document_processor/run.py
    ```
    
    Submit it to a Xeon node:
    ```bash
    qsub -l nodes=1:ppn=2 -d . job.sh
    ```

---

## 3. Docker Deployment (Containerized)

For production-grade deployment.

### 1. Create `Dockerfile`
Save this as `Dockerfile` in the root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY examples/ examples/

# Set Python path
ENV PYTHONPATH=/app/src

# Default command
CMD ["python", "examples/agents/document_processor/run.py"]
```

### 2. Build and Run
```bash
docker build -t aiwork-agent .
docker run aiwork-agent
```
