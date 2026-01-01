from aiwork.core.agent import Agent
from aiwork.core.memory import VectorMemory


def test_agent_execute_task_returns_expected_string():
    agent = Agent(role="Analyst", goal="Analyze", backstory="Backstory", verbose=False)
    result = agent.execute_task("do work", {})
    assert "Agent Analyst Result" in result
    assert "do work" in result


def test_agent_with_memory_does_not_error():
    memory = VectorMemory()
    memory.add("The sky is blue")
    agent = Agent(role="Detective", goal="Find", backstory="Backstory", memory=memory, verbose=False)
    result = agent.execute_task("sky", {})
    assert "sky" in result
