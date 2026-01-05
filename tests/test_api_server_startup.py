"""Tests for API server startup and port binding."""

import pytest
import threading
import time
import requests
from aiwork.api.server import app, is_port_available, find_available_port


def test_is_port_available():
    """Test port availability checking."""
    # Port 0 should be available (OS assigns random port)
    assert is_port_available(0)
    
    # Very high port should be available
    assert is_port_available(65000)


def test_find_available_port():
    """Test finding available port."""
    port = find_available_port(start_port=50000)
    assert port is not None
    assert port >= 50000


def test_server_starts_and_responds():
    """Test that server starts and responds to health check."""
    port = find_available_port(50000)
    assert port is not None
    
    # Start server in background thread
    def run_server():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    # Test health check
    try:
        response = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server did not respond: {e}")


def test_server_handles_port_conflict():
    """Test graceful handling of port already in use."""
    from aiwork.api.server import start_server
    
    port = find_available_port(50100)
    
    # Start first server
    def run_server():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # Try to start second server on same port - should fail gracefully
    with pytest.raises(OSError, match=r"Port \d+ is already in use\. Use --auto-port to find alternative\."):
        start_server(host="127.0.0.1", port=port, auto_port=False)


def test_is_port_available_with_occupied_port():
    """Test that is_port_available returns False for occupied ports."""
    port = find_available_port(50200)
    
    # Start server to occupy port
    def run_server():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # Port should now be unavailable
    assert not is_port_available(port, "127.0.0.1")


def test_find_available_port_range():
    """Test finding available port within range."""
    # Start several servers to occupy ports
    start_port = 50300
    occupied_ports = []
    threads = []
    
    for i in range(3):
        port = start_port + i
        
        # Use default argument to capture port value correctly
        def run_server(p=port):
            app.run(host="127.0.0.1", port=p, debug=False, use_reloader=False)
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        threads.append(thread)
        occupied_ports.append(port)
    
    time.sleep(0.5)
    
    # Find available port should skip occupied ones
    available = find_available_port(start_port, max_attempts=10)
    assert available is not None
    assert available >= start_port + 3
