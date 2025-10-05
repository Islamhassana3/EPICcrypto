"""
Integration test for port finding in launch scripts
"""
import sys
import os
import socket
import subprocess
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_find_port_script_default():
    """Test find_port.py with default port"""
    result = subprocess.run(
        ['python3', 'find_port.py', '5000'],
        capture_output=True,
        text=True,
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    assert result.returncode == 0, f"Script should succeed, got return code {result.returncode}"
    port = int(result.stdout.strip())
    assert port >= 5000, f"Port should be >= 5000, got {port}"
    print(f"✓ find_port.py returned port {port}")
    return True


def test_find_port_script_with_occupied_port():
    """Test find_port.py when port is occupied"""
    test_port = 6000
    
    # Occupy the port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', test_port))
    server_socket.listen(1)
    
    try:
        result = subprocess.run(
            ['python3', 'find_port.py', str(test_port)],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        assert result.returncode == 0, f"Script should succeed, got return code {result.returncode}"
        port = int(result.stdout.strip())
        assert port != test_port, f"Should return different port than {test_port}, got {port}"
        assert port > test_port, f"Should return higher port than {test_port}, got {port}"
        print(f"✓ find_port.py correctly found alternative port {port} when {test_port} was occupied")
        return True
    finally:
        server_socket.close()


def test_bash_script_syntax():
    """Test that bash script has valid syntax"""
    script_path = os.path.join(os.path.dirname(__file__), '..', 'preview.sh')
    result = subprocess.run(
        ['bash', '-n', script_path],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Bash script has syntax errors: {result.stderr}"
    print("✓ preview.sh has valid syntax")
    return True


def test_powershell_script_syntax():
    """Test that PowerShell script has valid syntax"""
    # Check if PowerShell is available
    pwsh_check = subprocess.run(
        ['pwsh', '-Version'],
        capture_output=True,
        text=True
    )
    
    if pwsh_check.returncode != 0:
        print("⚠ PowerShell not available, skipping syntax check")
        return True
    
    script_path = os.path.join(os.path.dirname(__file__), '..', 'preview.ps1')
    result = subprocess.run(
        ['pwsh', '-NoProfile', '-NonInteractive', '-Command',
         f'$null = [System.Management.Automation.PSParser]::Tokenize((Get-Content {script_path} -Raw), [ref]$null); exit 0'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"PowerShell script has syntax errors"
    print("✓ preview.ps1 has valid syntax")
    return True


def test_port_finder_module():
    """Test that port_finder module works correctly"""
    from backend.utils.port_finder import find_available_port, is_port_available
    
    # Test with a high port number that should be free
    test_port = 54321
    port = find_available_port(test_port)
    assert port == test_port, f"Should return preferred port {test_port} when available, got {port}"
    
    print(f"✓ Port finder module works correctly")
    return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*50)
    print("Running Integration Tests for Port Finding")
    print("="*50 + "\n")
    
    tests = [
        ("find_port.py default", test_find_port_script_default),
        ("find_port.py with occupied port", test_find_port_script_with_occupied_port),
        ("bash script syntax", test_bash_script_syntax),
        ("PowerShell script syntax", test_powershell_script_syntax),
        ("port_finder module", test_port_finder_module),
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
            import traceback
            traceback.print_exc()
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
