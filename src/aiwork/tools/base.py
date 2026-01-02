from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    name: str
    description: str
    input_schema: Dict[str, Any]

    @abstractmethod
    def run(self, input: Dict[str, Any]) -> Any:
        pass
