"""Tests for LLM integration."""

import pytest
from aiwork.core.llm import BaseLLM, MockLLM
from aiwork.core.agent import Agent


def test_mock_llm_generate():
    """Test MockLLM generates responses."""
    llm = MockLLM()
    response = llm.generate("Test prompt")
    assert "Mock LLM Response" in response
    assert llm.call_count == 1


def test_mock_llm_custom_responses():
    """Test MockLLM with custom response mapping."""
    llm = MockLLM(responses={"research": "Custom research response"})
    response = llm.generate("research papers on AI")
    assert response == "Custom research response"


def test_mock_llm_chat():
    """Test MockLLM chat method."""
    llm = MockLLM(responses={"hello": "Hi there!"})
    messages = [{"role": "user", "content": "hello world"}]
    response = llm.chat(messages)
    assert response == "Hi there!"


def test_agent_with_llm():
    """Test agent uses LLM when available."""
    llm = MockLLM(responses={"task": "LLM-generated result"})
    agent = Agent(
        role="Tester",
        goal="Test LLM integration",
        backstory="Test agent",
        llm=llm,
        verbose=False
    )
    
    result = agent.execute_task("Perform task", {})
    assert "LLM-generated result" in result


def test_agent_without_llm():
    """Test agent works without LLM (deterministic mode)."""
    agent = Agent(
        role="Tester",
        goal="Test without LLM",
        backstory="Test agent",
        llm=None,
        verbose=False
    )
    
    result = agent.execute_task("Perform task", {})
    assert "Tester" in result
    assert "Processed" in result


def test_agent_llm_fallback_on_error():
    """Test agent falls back gracefully when LLM fails."""
    class FailingLLM(BaseLLM):
        def generate(self, prompt: str, **kwargs) -> str:
            raise Exception("LLM error")
        
        def chat(self, messages, **kwargs) -> str:
            raise Exception("LLM error")
    
    agent = Agent(
        role="Tester",
        goal="Test LLM fallback",
        backstory="Test agent",
        llm=FailingLLM(),
        verbose=False
    )
    
    result = agent.execute_task("Test task", {})
    assert "LLM unavailable" in result
    assert "Tester" in result


def test_mock_llm_increments_call_count():
    """Test MockLLM tracks call count."""
    llm = MockLLM()
    llm.generate("First call")
    llm.generate("Second call")
    llm.generate("Third call")
    assert llm.call_count == 3


def test_agent_with_llm_and_memory():
    """Test agent stores LLM interactions in memory."""
    from aiwork.core.memory import VectorMemory
    
    llm = MockLLM(responses={"analyze": "Analysis complete"})
    memory = VectorMemory()
    agent = Agent(
        role="Analyst",
        goal="Analyze data",
        backstory="Expert analyst",
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    result = agent.execute_task("Analyze this data", {})
    assert "Analysis complete" in result
    
    # Verify memory was updated
    memories = memory.search("Analyze")
    assert len(memories) > 0
