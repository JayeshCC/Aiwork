from typing import Any, Callable, Optional

class Guardrail:
    """
    Enforces safety and validation policies on Task inputs and outputs.
    """
    def __init__(self, name: str, validator: Callable[[Any], bool], description: str = ""):
        self.name = name
        self.validator = validator
        self.description = description

    def validate(self, data: Any) -> bool:
        """
        Runs the validation logic. Returns True if valid, False otherwise.
        """
        try:
            return self.validator(data)
        except Exception as e:
            print(f"Guardrail {self.name} Error: {e}")
            return False
