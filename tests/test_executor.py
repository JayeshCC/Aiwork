from aiwork.executors.local_executor import LocalExecutor


def test_local_executor_executes_tasks():
    executor = LocalExecutor(max_workers=2)
    tasks = [
        lambda ctx: ctx["val"] + 1,
        lambda ctx: ctx["val"] * 2,
    ]
    results = executor.execute_tasks(tasks, {"val": 2})
    assert set(results) == {3, 4}
