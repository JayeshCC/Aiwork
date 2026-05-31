# Problem Statement - 2

# Build-Your-Own AI Agent Framework

Build an **AI Agent framework** (not just an app) that can orchestrate **agentic workflows** from input to
output without using existing agent frameworks like crew.ai, AutoGen, or n8n. The framework should
support allowing the definition of agentic workflows as a composition of **task flows**. These must then be
executable. Must be able to monitor and audit them. Apache projects can be used for orchestration,
messaging, and storage.

#### **High-Level Guidelines**

- **Core Features** :
    - Define and execute **task flows** (DAG or state machine).
    - Support **input handlers** , **tools/actions** , and **output actions**.
    - Include **memory** , **guardrails** , and **observability** (logs, metrics).
- **Architecture** :
    - Ingress (REST/queue) → Orchestrator → Executors → State/Memory.
    - Use Apache components (Kafka, Airflow, Camel, etc.) for messaging and orchestration.
- **Intel Tech** :
    - Develop and benchmark on **Intel® DevCloud**.
    - Optimize any ML models (LLMs, re-rankers, OCR) with **Intel® OpenVINO™**.
- **Deliverables** :
    - Framework SDK with APIs for flows, tools, and policies.
    - At least **two reference agents** demonstrated real workflows.
    - Design doc + performance benchmarks (pre/post optimization).
- **Performance Targets** :
    - Reliable execution with retries and timeouts.
    - Demonstrate Intel optimizations if ML is involved.
- **Stretch Goals** :
    - Multi-agent collaboration, reflection loops, human-in-the-loop steps.


