import pytest
import json
import time
from aiwork.api.server import app, workflow_store, task_store, store_lock


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Clear stores after each test
    with store_lock:
        workflow_store.clear()
        task_store.clear()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert data["framework"] == "AIWork"


def test_submit_workflow(client):
    """Test submitting a workflow via POST /workflow."""
    workflow_data = {
        "name": "test_workflow",
        "tasks": [
            {"name": "task1", "depends_on": []},
            {"name": "task2", "depends_on": ["task1"]}
        ],
        "context": {"input": "test_value"}
    }
    
    response = client.post('/workflow',
                          data=json.dumps(workflow_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data
    assert data["status"] == "PENDING"
    assert "message" in data


def test_get_workflow_status(client):
    """Test getting workflow status via GET /workflow/{id}."""
    # Submit a workflow first
    workflow_data = {
        "name": "status_test_workflow",
        "tasks": [
            {"name": "task1", "depends_on": []}
        ],
        "context": {}
    }
    
    response = client.post('/workflow',
                          data=json.dumps(workflow_data),
                          content_type='application/json')
    workflow_id = json.loads(response.data)["id"]
    
    # Get status
    response = client.get(f'/workflow/{workflow_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == workflow_id
    assert data["name"] == "status_test_workflow"
    assert data["status"] in ["PENDING", "RUNNING", "COMPLETED"]


def test_get_workflow_status_not_found(client):
    """Test getting status for non-existent workflow."""
    response = client.get('/workflow/non-existent-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


def test_workflow_completion(client):
    """Test that workflow completes and outputs are available."""
    workflow_data = {
        "name": "completion_test",
        "tasks": [
            {"name": "task1", "depends_on": []}
        ],
        "context": {}
    }
    
    response = client.post('/workflow',
                          data=json.dumps(workflow_data),
                          content_type='application/json')
    workflow_id = json.loads(response.data)["id"]
    
    # Wait for workflow to complete (with timeout)
    max_attempts = 10
    for _ in range(max_attempts):
        time.sleep(0.5)
        response = client.get(f'/workflow/{workflow_id}')
        data = json.loads(response.data)
        if data["status"] == "COMPLETED":
            assert "tasks" in data
            assert "task1" in data["tasks"]
            assert data["tasks"]["task1"]["status"] == "COMPLETED"
            break
    else:
        pytest.fail("Workflow did not complete in time")


def test_get_task_result_not_found(client):
    """Test getting result for non-existent task."""
    response = client.get('/task/non-existent-task-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


def test_submit_workflow_invalid_data(client):
    """Test submitting workflow with invalid data."""
    # Missing 'name' field
    invalid_data = {
        "tasks": [{"name": "task1"}]
    }
    
    response = client.post('/workflow',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_submit_workflow_invalid_task(client):
    """Test submitting workflow with invalid task data."""
    # Task missing 'name' field
    invalid_data = {
        "name": "test_workflow",
        "tasks": [{"depends_on": []}]
    }
    
    response = client.post('/workflow',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
