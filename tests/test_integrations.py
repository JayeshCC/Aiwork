from aiwork.core.flow import Flow
from aiwork.core.task import Task
from aiwork.integrations.kafka_adapter import KafkaAdapter
from aiwork.integrations.airflow_exporter import AirflowExporter
from aiwork.integrations.openvino_adapter import OpenVINOAdapter


def test_kafka_adapter_produce_and_consume():
    adapter = KafkaAdapter(bootstrap_servers="localhost:9092")
    adapter.produce_task("tasks", {"id": "1"})
    tasks = list(adapter.consume_tasks("tasks"))
    assert len(tasks) == 2
    assert tasks[0]["task_id"] == "1"


def test_airflow_exporter_writes_dag(tmp_path):
    flow = Flow("airflow_test")
    flow.add_task(Task("ingest", lambda c: None))
    flow.add_task(Task("process", lambda c: None), depends_on=["ingest"])

    output_path = tmp_path / "dag.py"
    AirflowExporter.export(flow, str(output_path))

    content = output_path.read_text()
    assert "airflow_test" in content
    assert "t_ingest" in content
    assert "t_process" in content
    assert "t_ingest >> t_process" in content


def test_openvino_adapter_infer_and_optimize():
    adapter = OpenVINOAdapter(model_path="model.xml")
    optimized = adapter.optimize_model(object())
    result = adapter.infer({"input": "data"})

    assert optimized == "OPTIMIZED_MODEL_REF"
    assert result["result"] == "inference_complete"
