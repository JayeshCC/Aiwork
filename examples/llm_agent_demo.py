"""
LLM-Powered Agent Demo
======================

Demonstrates agents with LLM integration:
- MockLLM for testing (no API key needed)
- OpenAILLM for production (requires API key)
- Automatic fallback if LLM unavailable
"""

from aiwork.core.agent import Agent
from aiwork.core.llm import MockLLM, OpenAILLM
from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

# Example 1: Agent with Mock LLM (always works)
print("=== Example 1: Mock LLM Agent ===\n")

mock_llm = MockLLM(responses={
    "research": "Based on recent papers, LLM agents show promise in tool use and planning.",
    "summarize": "Key findings: Agents can decompose tasks, use tools, and maintain context."
})

researcher = Agent(
    role="AI Researcher",
    goal="Research and summarize AI agent papers",
    backstory="PhD in AI with focus on agent systems",
    llm=mock_llm
)

def research_task(ctx):
    """Task that uses agent's LLM reasoning."""
    query = ctx.get("query", "AI agents")
    return researcher.execute_task(f"Research papers on: {query}", ctx)

task = Task("research", handler=research_task, agent=researcher)
flow = Flow("research_flow")
flow.add_task(task)

orchestrator = Orchestrator()
result = orchestrator.execute(flow, {"query": "LLM agent frameworks"})

print(f"\nResult: {result['outputs']['research']}\n")

# Example 2: Try OpenAI (graceful fallback if no API key)
print("=== Example 2: OpenAI LLM Agent (Optional) ===\n")

try:
    openai_llm = OpenAILLM(model="gpt-3.5-turbo")
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze data and provide insights",
        backstory="Expert in statistical analysis",
        llm=openai_llm
    )
    print("✅ OpenAI LLM initialized")
except Exception as e:
    print(f"⚠️  OpenAI unavailable: {e}")
    print("Using agent without LLM (deterministic mode)")
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze data",
        backstory="Expert analyst",
        llm=None
    )

# Demonstrate deterministic mode
print("\n=== Example 3: Agent Without LLM ===\n")

simple_agent = Agent(
    role="Simple Agent",
    goal="Process tasks deterministically",
    backstory="Basic task processor",
    llm=None
)

result = simple_agent.execute_task("Process this task", {})
print(f"\nDeterministic Result: {result}")
