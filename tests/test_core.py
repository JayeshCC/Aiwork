import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator

class TestCore(unittest.TestCase):
    def test_task_execution(self):
        def handler(ctx):
            return "success"
        task = Task("test_task", handler)
        self.assertEqual(task.execute({}), "success")
        self.assertEqual(task.status, "COMPLETED")

    def test_flow_dag(self):
        flow = Flow("test_flow")
        t1 = Task("t1", lambda c: 1)
        t2 = Task("t2", lambda c: 2)
        flow.add_task(t1)
        flow.add_task(t2, depends_on=["t1"])
        
        sorted_tasks = flow.get_topological_sort()
        self.assertEqual(len(sorted_tasks), 2)
        self.assertEqual(sorted_tasks[0].name, "t1")
        self.assertEqual(sorted_tasks[1].name, "t2")

    def test_orchestrator(self):
        flow = Flow("orch_flow")
        flow.add_task(Task("A", lambda c: "A"))
        flow.add_task(Task("B", lambda c: c["outputs"]["A"] + "B"), depends_on=["A"])
        
        orch = Orchestrator()
        res = orch.execute(flow, {})
        self.assertEqual(res["outputs"]["B"], "AB")

if __name__ == '__main__':
    unittest.main()
