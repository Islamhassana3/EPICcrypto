"""
Utility module for finding available network ports
"""
import socket
import logging

logger = logging.getLogger(__name__)


def is_port_available(port, host='0.0.0.0'):
    """
    Check if a port is available for binding.
    
    Args:
        port (int): Port number to check
        host (str): Host address to bind to (default: '0.0.0.0')
    
    Returns:
        bool: True if port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
    except (OSError, socket.error):
        return False


def find_available_port(preferred_port=5000, host='0.0.0.0', max_attempts=10):
    """
    Find an available port, starting with the preferred port.
    
    Args:
        preferred_port (int): The preferred port to try first (default: 5000)
        host (str): Host address to bind to (default: '0.0.0.0')
        max_attempts (int): Maximum number of ports to try (default: 10)
    
    Returns:
        int: An available port number
    
    Raises:
        RuntimeError: If no available port is found after max_attempts
    """
    # First try the preferred port
    if is_port_available(preferred_port, host):
        logger.info(f"Port {preferred_port} is available")
        return preferred_port
    
    logger.warning(f"Port {preferred_port} is already in use, searching for alternative...")
    
    # Try sequential ports after the preferred port
    for i in range(1, max_attempts):
        candidate_port = preferred_port + i
        if is_port_available(candidate_port, host):
            logger.info(f"Found available port: {candidate_port}")
            return candidate_port
    
    raise RuntimeError(
        f"Could not find an available port after checking {max_attempts} ports "
        f"starting from {preferred_port}"
    )
