import pytest

from aiwork.tools.registry import ToolRegistry


def test_tool_registry_register_and_get():
    registry = ToolRegistry()

    @registry.register("hello")
    def hello():
        return "world"

    tool = registry.get_tool("hello")
    assert tool() == "world"
    assert "hello" in registry.list_tools()


def test_tool_registry_missing_tool():
    registry = ToolRegistry()
    with pytest.raises(ValueError):
        registry.get_tool("missing")
