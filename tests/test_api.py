from aiwork.api.server import health_check, execute_flow, FlowRequest, TaskDefinition


def test_health_check():
    res = health_check()
    assert res["status"] == "healthy"
    assert res["framework"] == "AIWork"


def test_execute_flow_returns_outputs():
    request = FlowRequest(
        flow_name="api_flow",
        tasks=[
            TaskDefinition(name="t1", depends_on=[]),
            TaskDefinition(name="t2", depends_on=["t1"]),
        ],
        input_context={"input": "value"},
    )

    result = execute_flow(request)
    assert result["status"] == "success"
    assert "t1" in result["outputs"]
    assert "t2" in result["outputs"]
