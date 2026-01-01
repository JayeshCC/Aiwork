import pytest

from aiwork.core.observability import MetricsRegistry, metrics
from aiwork.observability.logger import Logger, monitor


def test_metrics_registry_is_singleton():
    r1 = MetricsRegistry()
    r2 = MetricsRegistry()
    assert r1 is r2


def test_metrics_record_and_summary():
    metrics.metrics.clear()
    metrics.record("task_duration_seconds", 1.23, {"task": "t1", "status": "success"})
    summary = metrics.get_summary()
    assert len(summary) == 1
    assert summary[0]["name"] == "task_duration_seconds"
    assert summary[0]["value"] == 1.23


def test_logger_info_and_monitor_success(caplog):
    log = Logger("aiwork-test")
    log.info("hello")

    @monitor
    def work():
        return "ok"

    with caplog.at_level("INFO"):
        result = work()
    assert result == "ok"


def test_monitor_logs_error_and_raises(caplog):
    @monitor
    def fail():
        raise ValueError("boom")

    with caplog.at_level("ERROR"):
        with pytest.raises(ValueError):
            fail()
