"""
Tests for port finder utility
"""
import sys
import os
import socket
import threading
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.port_finder import is_port_available, find_available_port


def test_is_port_available():
    """Test checking if a port is available"""
    # Try to find a port that should be available (high port number)
    test_port = 55555
    
    # First check should be available
    assert is_port_available(test_port), f"Port {test_port} should be available"
    
    # Occupy the port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', test_port))
    server_socket.listen(1)
    
    # Now it should not be available
    assert not is_port_available(test_port), f"Port {test_port} should not be available"
    
    # Clean up
    server_socket.close()
    time.sleep(0.1)  # Give OS time to release the port
    
    print("✓ is_port_available works correctly")
    return True


def test_find_available_port_preferred_free():
    """Test finding available port when preferred port is free"""
    test_port = 55556
    
    # Ensure port is free
    if not is_port_available(test_port):
        print(f"⚠ Warning: Port {test_port} is not available, skipping test")
        return True
    
    result = find_available_port(preferred_port=test_port)
    assert result == test_port, f"Should return preferred port {test_port}, got {result}"
    
    print("✓ find_available_port returns preferred port when free")
    return True


def test_find_available_port_preferred_occupied():
    """Test finding available port when preferred port is occupied"""
    test_port = 55557
    
    # Occupy the preferred port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', test_port))
    server_socket.listen(1)
    
    try:
        # Should find an alternative port
        result = find_available_port(preferred_port=test_port, max_attempts=5)
        assert result > test_port, f"Should return a port greater than {test_port}, got {result}"
        assert result <= test_port + 5, f"Should return a port within range, got {result}"
        
        print(f"✓ find_available_port found alternative port {result} when {test_port} was occupied")
        return True
    finally:
        server_socket.close()


def test_find_available_port_no_ports_available():
    """Test that RuntimeError is raised when no ports are available"""
    test_port = 55558
    max_attempts = 3
    
    # Occupy multiple ports
    sockets = []
    for i in range(max_attempts):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', test_port + i))
        s.listen(1)
        sockets.append(s)
    
    try:
        # Should raise RuntimeError
        try:
            result = find_available_port(preferred_port=test_port, max_attempts=max_attempts)
            assert False, f"Should have raised RuntimeError, but got port {result}"
        except RuntimeError as e:
            assert "Could not find an available port" in str(e)
            print("✓ find_available_port raises RuntimeError when no ports available")
            return True
    finally:
        for s in sockets:
            s.close()


def run_all_tests():
    """Run all port finder tests"""
    print("\n" + "="*50)
    print("Running Port Finder Tests")
    print("="*50 + "\n")
    
    tests = [
        ("is_port_available", test_is_port_available),
        ("find_available_port - preferred free", test_find_available_port_preferred_free),
        ("find_available_port - preferred occupied", test_find_available_port_preferred_occupied),
        ("find_available_port - no ports available", test_find_available_port_no_ports_available),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 50)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*50 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
