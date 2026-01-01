import time
import importlib.util
import os


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_benchmark_model_returns_speedup():
    module = load_module(os.path.join("benchmarks", "openvino_benchmark.py"), "openvino_benchmark")

    def baseline():
        time.sleep(0.001)

    def optimized():
        time.sleep(0.0005)

    speedup = module.benchmark_model("test", baseline, optimized, iterations=2)
    assert speedup > 0
