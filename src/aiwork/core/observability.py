import time
from typing import Dict, Any

class MetricsRegistry:
    """
    Singleton registry for collecting system metrics.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsRegistry, cls).__new__(cls)
            cls._instance.metrics = []
        return cls._instance

    def record(self, name: str, value: float, tags: Dict[str, str] = None):
        entry = {
            "timestamp": time.time(),
            "name": name,
            "value": value,
            "tags": tags or {}
        }
        self.metrics.append(entry)
        # In a real system, this would push to Prometheus/Datadog
        # print(f"[Metrics] {name}: {value} {tags}")

    def get_summary(self):
        return self.metrics

# Global instance
metrics = MetricsRegistry()
