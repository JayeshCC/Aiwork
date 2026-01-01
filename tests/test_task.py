import pytest

from aiwork.core.task import Task
from aiwork.core.guardrail import Guardrail


def test_task_uses_agent_when_no_handler():
    class DummyAgent:
        def execute_task(self, desc, context):
            return f"agent:{desc}"

    task = Task("t1", "do work", agent=DummyAgent())
    result = task.execute({})
    assert result == "agent:do work"
    assert task.status == "COMPLETED"


def test_task_guardrail_failure_raises():
    def handler(_):
        return {"raw_text": "no currency"}

    guard = Guardrail("has_dollar", lambda d: "$" in d.get("raw_text", ""))
    task = Task("t2", handler, guardrails=[guard])

    with pytest.raises(ValueError):
        task.execute({})
