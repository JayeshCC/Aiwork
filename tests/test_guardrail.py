from aiwork.core.guardrail import Guardrail
from aiwork.core.task import Task
import pytest


def test_guardrail_validate_true():
    guard = Guardrail("always_true", lambda d: True)
    assert guard.validate({"value": 1}) is True


def test_guardrail_validate_exception_returns_false():
    def bad_validator(_):
        raise RuntimeError("bad")

    guard = Guardrail("bad", bad_validator)
    assert guard.validate({"value": 1}) is False


def test_input_guardrail_validation():
    """Test input guardrails validate before execution."""
    guard = Guardrail(
        name="positive_value",
        validator=lambda ctx: ctx.get("value", 0) > 0
    )
    
    task = Task(
        name="test",
        handler=lambda ctx: {"result": ctx["value"] * 2},
        input_guardrails=[guard],
        retries=0
    )
    
    # Valid input - should succeed
    result = task.execute({"value": 5})
    assert result["result"] == 10
    
    # Invalid input - should fail
    with pytest.raises(ValueError) as exc:
        task.execute({"value": -5})
    assert "Input guardrail" in str(exc.value)


def test_both_input_and_output_guardrails():
    """Test task with both input and output validation."""
    input_guard = Guardrail(
        name="input_check",
        validator=lambda ctx: "value" in ctx
    )
    
    output_guard = Guardrail(
        name="output_check",
        validator=lambda result: isinstance(result, dict)
    )
    
    task = Task(
        name="test",
        handler=lambda ctx: {"processed": ctx["value"]},
        input_guardrails=[input_guard],
        guardrails=[output_guard],
        retries=0
    )
    
    # Valid input and output
    result = task.execute({"value": 42})
    assert result["processed"] == 42
    
    # Invalid input
    with pytest.raises(ValueError):
        task.execute({})  # Missing "value" key
