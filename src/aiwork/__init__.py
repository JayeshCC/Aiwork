"""
AIWork: Lightweight AI Agent Framework

A production-ready Python framework for orchestrating AI agent workflows,
optimized for Intel hardware.
"""

__version__ = "0.1.0"

from .core.task import Task
from .core.flow import Flow
from .core.agent import Agent
from .core.guardrail import Guardrail
from .core.memory import Memory, VectorMemory
from .orchestrator import Orchestrator

__all__ = [
    "Task",
    "Flow",
    "Agent",
    "Guardrail",
    "Memory",
    "VectorMemory",
    "Orchestrator",
]
