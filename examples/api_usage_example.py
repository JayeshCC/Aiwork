#!/usr/bin/env python
"""
Example usage of the AIWork REST API

This script demonstrates how to:
1. Submit a workflow via POST /workflow
2. Check workflow status via GET /workflow/{id}
3. Retrieve task results via GET /task/{id}

Make sure the server is running:
    python -m aiwork.api.server
"""

import requests
import time
import json

BASE_URL = "http://localhost:5000"

def example_simple_workflow():
    """Submit and monitor a simple workflow"""
    print("=" * 60)
    print("Example: Simple Workflow Submission")
    print("=" * 60)
    
    # Define workflow
    workflow_data = {
        "name": "example_workflow",
        "tasks": [
            {"name": "task1", "depends_on": []},
            {"name": "task2", "depends_on": ["task1"]},
            {"name": "task3", "depends_on": ["task1", "task2"]}
        ],
        "context": {"input": "example_data"}
    }
    
    # Submit workflow
    print("\n1. Submitting workflow...")
    response = requests.post(f"{BASE_URL}/workflow", json=workflow_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    workflow_id = result["id"]
    
    # Poll for completion
    print("\n2. Checking workflow status...")
    for i in range(10):
        time.sleep(0.5)
        response = requests.get(f"{BASE_URL}/workflow/{workflow_id}")
        result = response.json()
        print(f"   Status: {result['status']}")
        
        if result["status"] in ["COMPLETED", "FAILED"]:
            print(f"\n3. Final result:")
            print(json.dumps(result, indent=2))
            break
    
    return workflow_id

def example_health_check():
    """Check API health"""
    print("\n" + "=" * 60)
    print("Example: Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def example_parallel_workflows():
    """Submit multiple workflows in parallel"""
    print("\n" + "=" * 60)
    print("Example: Parallel Workflow Execution")
    print("=" * 60)
    
    workflow_ids = []
    
    # Submit multiple workflows
    print("\n1. Submitting 3 workflows in parallel...")
    for i in range(3):
        workflow_data = {
            "name": f"parallel_workflow_{i}",
            "tasks": [
                {"name": f"task_{i}_1", "depends_on": []},
                {"name": f"task_{i}_2", "depends_on": [f"task_{i}_1"]}
            ],
            "context": {"workflow_number": i}
        }
        
        response = requests.post(f"{BASE_URL}/workflow", json=workflow_data)
        result = response.json()
        workflow_ids.append(result["id"])
        print(f"   Submitted workflow {i}: {result['id'][:8]}...")
    
    # Wait for all to complete
    print("\n2. Waiting for all workflows to complete...")
    time.sleep(1)
    
    # Check status of all workflows
    print("\n3. Final status of all workflows:")
    for i, wid in enumerate(workflow_ids):
        response = requests.get(f"{BASE_URL}/workflow/{wid}")
        result = response.json()
        print(f"   Workflow {i}: {result['status']}")

if __name__ == "__main__":
    try:
        # Check if server is running
        example_health_check()
        
        # Run examples
        example_simple_workflow()
        example_parallel_workflows()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server at", BASE_URL)
        print("Please start the server with: python -m aiwork.api.server")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
