"""
Tests for the Executor Pattern implementation.

This test suite validates the separation of concerns between:
- Tasks: Define WHAT work to do
- Executors: Define HOW to execute tasks
"""
import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.executors.base_executor import BaseExecutor
from aiwork.executors.local_executor import LocalExecutor
from aiwork.orchestrator import Orchestrator
from aiwork.core.guardrail import Guardrail


class TestExecutorPattern(unittest.TestCase):
    """Test the executor pattern implementation."""
    
    def test_base_executor_is_abstract(self):
        """Verify BaseExecutor cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            BaseExecutor()
    
    def test_local_executor_implements_base_executor(self):
        """Verify LocalExecutor properly implements BaseExecutor."""
        executor = LocalExecutor()
        self.assertIsInstance(executor, BaseExecutor)
        self.assertTrue(hasattr(executor, 'execute'))
    
    def test_executor_executes_task(self):
        """Test executor can execute a task."""
        executor = LocalExecutor()
        
        def handler(ctx):
            return "executed"
        
        task = Task("test_task", handler)
        result = executor.execute(task, {})
        
        self.assertEqual(result, "executed")
        self.assertEqual(task.status, "COMPLETED")
        self.assertEqual(task.output, "executed")
    
    def test_executor_handles_task_with_agent(self):
        """Test executor works with agent-based tasks."""
        class DummyAgent:
            def execute_task(self, desc, context):
                return f"agent_result:{desc}"
        
        executor = LocalExecutor()
        task = Task("agent_task", "process data", agent=DummyAgent())
        result = executor.execute(task, {})
        
        self.assertEqual(result, "agent_result:process data")
        self.assertEqual(task.status, "COMPLETED")
    
    def test_executor_implements_retry_logic(self):
        """Test executor properly implements retry logic."""
        executor = LocalExecutor()
        
        attempt_count = [0]
        def failing_handler(ctx):
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ValueError("Temporary failure")
            return "success_after_retries"
        
        task = Task("retry_task", failing_handler, retries=3)
        result = executor.execute(task, {})
        
        self.assertEqual(result, "success_after_retries")
        self.assertEqual(task.status, "COMPLETED")
        self.assertEqual(attempt_count[0], 3)
    
    def test_executor_respects_retry_limit(self):
        """Test executor fails after max retries."""
        executor = LocalExecutor()
        
        def always_failing_handler(ctx):
            raise ValueError("Persistent failure")
        
        task = Task("failing_task", always_failing_handler, retries=2)
        
        with self.assertRaises(ValueError) as cm:
            executor.execute(task, {})
        
        self.assertEqual(str(cm.exception), "Persistent failure")
        self.assertEqual(task.status, "FAILED")
        self.assertEqual(task.error, "Persistent failure")
    
    def test_executor_validates_guardrails(self):
        """Test executor validates output guardrails."""
        executor = LocalExecutor()
        
        def handler(ctx):
            return {"value": 5}
        
        guard = Guardrail("positive", lambda d: d.get("value", 0) > 0)
        task = Task("guarded_task", handler, guardrails=[guard])
        
        result = executor.execute(task, {})
        self.assertEqual(result, {"value": 5})
        self.assertEqual(task.status, "COMPLETED")
    
    def test_executor_fails_on_guardrail_violation(self):
        """Test executor properly fails when guardrails are violated."""
        executor = LocalExecutor()
        
        def handler(ctx):
            return {"value": -5}
        
        guard = Guardrail("positive", lambda d: d.get("value", 0) > 0)
        task = Task("guarded_task", handler, guardrails=[guard])
        
        with self.assertRaises(ValueError) as cm:
            executor.execute(task, {})
        
        self.assertIn("Guardrail 'positive' failed", str(cm.exception))
        self.assertEqual(task.status, "FAILED")
    
    def test_orchestrator_uses_executor(self):
        """Test orchestrator properly uses executor for task execution."""
        executor = LocalExecutor()
        orchestrator = Orchestrator(executor=executor)
        
        flow = Flow("test_flow")
        flow.add_task(Task("task1", lambda c: "result1"))
        
        result = orchestrator.execute(flow, {})
        
        self.assertEqual(result["outputs"]["task1"], "result1")
    
    def test_orchestrator_defaults_to_local_executor(self):
        """Test orchestrator creates LocalExecutor by default."""
        orchestrator = Orchestrator()
        
        self.assertIsInstance(orchestrator.executor, LocalExecutor)
    
    def test_custom_executor_can_be_injected(self):
        """Test that custom executors can be injected into orchestrator."""
        class CustomExecutor(BaseExecutor):
            def __init__(self):
                self.executed_tasks = []
            
            def execute(self, task, context):
                self.executed_tasks.append(task.name)
                return task._run_handler(context)
        
        custom_executor = CustomExecutor()
        orchestrator = Orchestrator(executor=custom_executor)
        
        flow = Flow("test_flow")
        flow.add_task(Task("custom_task", lambda c: "custom_result"))
        
        result = orchestrator.execute(flow, {})
        
        self.assertEqual(result["outputs"]["custom_task"], "custom_result")
        self.assertIn("custom_task", custom_executor.executed_tasks)
    
    def test_task_internal_run_handler_method(self):
        """
        Test _run_handler is internal and works correctly.
        
        This test intentionally calls the internal _run_handler method
        to verify the task's core logic is separated from execution concerns.
        In production, this method is called by executors, not directly.
        """
        def handler(ctx):
            return ctx.get("input", "default")
        
        task = Task("test_task", handler)
        result = task._run_handler({"input": "value"})
        
        self.assertEqual(result, "value")
    
    def test_separation_of_concerns(self):
        """Test that tasks don't contain execution logic."""
        task = Task("test_task", lambda c: "result")
        
        # Task should NOT have direct retry/metrics logic
        # Those are in executor.execute()
        self.assertFalse(hasattr(task, 'attempt'))
        
        # Task should have core attributes
        self.assertTrue(hasattr(task, 'name'))
        self.assertTrue(hasattr(task, 'handler'))
        self.assertTrue(hasattr(task, 'retries'))
        self.assertTrue(hasattr(task, 'guardrails'))
        self.assertTrue(hasattr(task, 'status'))


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility of deprecated Task.execute()."""
    
    def test_deprecated_task_execute_still_works(self):
        """Test deprecated Task.execute() method still works."""
        import warnings
        
        task = Task("test_task", lambda c: "result")
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = task.execute({})
            
            # Verify deprecation warning was issued
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("deprecated", str(w[0].message).lower())
        
        # Verify it still works
        self.assertEqual(result, "result")
        self.assertEqual(task.status, "COMPLETED")


if __name__ == '__main__':
    unittest.main()
