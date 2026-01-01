from aiwork.core.agent import Agent
from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.core.memory import VectorMemory
from aiwork.orchestrator import Orchestrator
from aiwork.core.observability import metrics

def main():
    print("=== AIWork Memory & Observability Demo ===\n")

    # 1. Setup Memory
    print("Initializing Vector Memory...")
    memory = VectorMemory()
    memory.add("The secret code is 42.")
    memory.add("Project deadline is Dec 31st.")
    memory.add("The sky is blue.")

    # 2. Setup Agent with Memory
    agent = Agent(
        role="Detective",
        goal="Find the secret",
        backstory="A detective who never forgets.",
        memory=memory
    )

    # 3. Define Task
    def find_secret(ctx):
        # The agent's execute_task method will be called automatically if no handler is provided,
        # but here we want to demonstrate the agent's internal logic being triggered by the Task.
        # However, Task.execute calls agent.execute_task if handler is missing.
        # Let's rely on the agent's default execution which prints the recalled memory.
        return "Secret Found"

    task = Task(
        name="search_memory",
        description="What is the secret code?",
        agent=agent
        # No handler provided, so it defaults to agent.execute_task
    )

    # 4. Execute Flow
    flow = Flow("memory_demo_flow")
    flow.add_task(task)

    orchestrator = Orchestrator()
    orchestrator.execute(flow)

    # 5. Check Metrics
    print("\n=== Observability Metrics ===")
    summary = metrics.get_summary()
    for m in summary:
        print(f"{m['name']}: {m['value']} ({m['tags']})")

if __name__ == "__main__":
    main()
