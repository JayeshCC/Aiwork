# 📘 AIWork User Guide

Welcome to **AIWork**, the lightweight, high-performance framework for building Agentic AI applications. This guide provides a detailed overview of the system, its capabilities, and how to use it to build intelligent workflows.

---

## 1. 🌟 Introduction

AIWork is designed to bridge the gap between simple automation scripts and complex, heavy enterprise frameworks. It provides a structured way to define **Agents**, **Tasks**, and **Workflows** that run efficiently on local hardware, with specific optimizations for **Intel® Architecture**.

### Why AIWork?
*   **Agent-Centric**: Build systems based on "who" does the work (Agents), not just "what" needs to be done.
*   **Hybrid Orchestration**: Combine predictable, static workflows with dynamic, AI-driven decision making.
*   **Hardware Accelerated**: Built-in integration with Intel OpenVINO™ for lightning-fast AI inference.
*   **Production Ready**: Includes retry logic, state management, and modular architecture.

---

## 2. 🧠 Core Concepts

### 🤖 Agents
Agents are the intelligent workers in your system. Unlike simple functions, an Agent has a persona.
*   **Role**: What is their job title? (e.g., "Financial Analyst")
*   **Goal**: What are they trying to achieve? (e.g., "Detect fraud in invoices")
*   **Backstory**: Context that guides their behavior.
*   **Tools**: Specific capabilities they can use (e.g., a Calculator, an OCR engine).

### 📋 Tasks
A Task is a specific unit of work. It connects an **Agent** to a **Goal**.
*   **Description**: A clear instruction of what needs to be done.
*   **Handler**: The logic (or AI prompt) used to execute the task.
*   **Dependencies**: What other tasks must finish before this one starts?

### twisted_rightwards_arrows Flows
A Flow is the roadmap for your application. It defines the sequence of tasks.
*   **Static Flows**: A fixed sequence (A -> B -> C). Great for standard processes.
*   **Dynamic Flows**: The Flow can change at runtime. An Agent can decide to add new tasks based on the data it sees.

### 🎼 Orchestrator
The Orchestrator is the engine that runs your Flows. It handles:
*   **Scheduling**: Figuring out which task to run next.
*   **Data Passing**: Moving outputs from one task to the inputs of the next.
*   **Error Handling**: Retrying failed tasks.

---

## 3. 🚀 Key Features

### Hybrid Orchestration
One of AIWork's most powerful features is **Hybrid Orchestration**.
*   **Scenario**: You have a standard invoice processing pipeline.
*   **Dynamic Behavior**: If an Agent detects a "High Value" invoice, it can dynamically inject a "Compliance Audit" task into the workflow *while it is running*.
*   **Benefit**: You don't need to build complex "If/Else" spaghetti code. The workflow adapts organically.

### Intel® OpenVINO™ Integration
AIWork comes with a pre-built adapter for OpenVINO.
*   **Performance**: Run AI models (like OCR or Text Classification) up to 4x faster on Intel CPUs and GPUs.
*   **Simplicity**: Use standard model formats without worrying about low-level optimization code.

---

## 4. 💡 Use Cases

### Use Case 1: Intelligent Document Processing
**Problem**: A company receives thousands of invoices in PDF format. Manual entry is slow and error-prone.

**Solution with AIWork**:
1.  **OCR Agent**: Uses OpenVINO to extract text from the PDF instantly.
2.  **Analyst Agent**: Reads the text, identifies the Vendor and Total Amount.
3.  **Compliance Agent (Dynamic)**: If the amount is > $1000, this agent steps in to verify the vendor against a trusted list.

### Use Case 2: Automated Customer Support
**Problem**: Support tickets need to be categorized and routed to the right department.

**Solution with AIWork**:
1.  **Triage Agent**: Reads the ticket and determines the category (Tech Support, Billing, Sales).
2.  **Routing Flow**: The Orchestrator sends the ticket to the specific sub-flow for that category.
3.  **Response Agent**: Drafts a reply based on the category's knowledge base.

---

## 5. 🛠️ Getting Started

### Prerequisites
*   Python 3.8+
*   Intel CPU (Recommended for OpenVINO features)

### Installation
AIWork is designed to be installed as a standard Python package.
(See `README.md` for specific command-line instructions).

### Defining Your First Agent
Instead of writing raw code, you define your workforce:

```python
# Conceptual Example
researcher = Agent(
    role="Researcher",
    goal="Find latest news on AI",
    tools=[SearchTool()]
)

task = Task(
    description="Research AI trends in 2024",
    agent=researcher
)

flow.add_task(task)
```

---

## 6. 📚 Best Practices

1.  **Single Responsibility**: Keep Agents focused on one specific domain.
2.  **Clear Goals**: Give Tasks specific, actionable descriptions.
3.  **Use Dynamic Flows Sparingly**: While powerful, dynamic flows can be harder to debug. Use them for exceptional cases (like Audits or Error Recovery).
4.  **Leverage OpenVINO**: Always use the OpenVINO adapter for heavy ML tasks to save compute resources.
