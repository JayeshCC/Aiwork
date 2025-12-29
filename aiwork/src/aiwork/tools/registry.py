from typing import Callable, Dict, Any

class ToolRegistry:
    """
    Registry for managing available tools (functions/skills) for agents.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str):
        """
        Decorator to register a function as a tool.
        """
        def decorator(func: Callable):
            self._tools[name] = func
            return func
        return decorator

    def get_tool(self, name: str) -> Callable:
        """
        Retrieves a tool by name.
        """
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def list_tools(self):
        """
        Lists all registered tools.
        """
        return list(self._tools.keys())

# Global registry instance
registry = ToolRegistry()
