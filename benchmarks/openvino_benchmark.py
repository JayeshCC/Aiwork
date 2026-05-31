import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.integrations.openvino_adapter import OpenVINOAdapter

def benchmark_model(name, framework_func, openvino_func, iterations=100):
    print(f"Starting simulated timing comparison for {name}...")
    
    # Baseline
    start = time.time()
    for _ in range(iterations):
        framework_func()
    end = time.time()
    baseline_avg = (end - start) / iterations * 1000
    print(f"  [{name}] Simulated standard latency: {baseline_avg:.2f} ms")

    # OpenVINO
    start = time.time()
    for _ in range(iterations):
        openvino_func()
    end = time.time()
    ov_avg = (end - start) / iterations * 1000
    print(f"  [{name}] Simulated OpenVINO-placeholder latency: {ov_avg:.2f} ms")
    
    speedup = baseline_avg / ov_avg
    print(f"  [{name}] Simulated timing ratio: {speedup:.2f}x")
    return speedup

def mock_pytorch_inference():
    time.sleep(0.045) # Simulate 45ms

def mock_openvino_inference():
    time.sleep(0.012) # Simulate 12ms

def main():
    print("=== Simulated OpenVINO Placeholder Timing Comparison ===\n")
    
    # Text Classification Benchmark
    s1 = benchmark_model("DistilBERT", mock_pytorch_inference, mock_openvino_inference)
    
    # OCR Benchmark
    def mock_ocr_standard():
        time.sleep(0.156)
    def mock_ocr_ov():
        time.sleep(0.042)
        
    s2 = benchmark_model("OCR Model", mock_ocr_standard, mock_ocr_ov)
    
    print("\n=== Summary ===")
    print(f"Average simulated timing ratio: {(s1+s2)/2:.2f}x")
    print("Simulation only: OpenVINO acceleration is not enabled or measured.")

if __name__ == "__main__":
    main()
