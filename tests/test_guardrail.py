from aiwork.core.guardrail import Guardrail


def test_guardrail_validate_true():
    guard = Guardrail("always_true", lambda d: True)
    assert guard.validate({"value": 1}) is True


def test_guardrail_validate_exception_returns_false():
    def bad_validator(_):
        raise RuntimeError("bad")

    guard = Guardrail("bad", bad_validator)
    assert guard.validate({"value": 1}) is False
