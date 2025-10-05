#!/usr/bin/env python3
"""
Simple script to find an available port.
Used by launch scripts to avoid port conflicts.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.port_finder import find_available_port


if __name__ == '__main__':
    preferred_port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    try:
        port = find_available_port(preferred_port)
        print(port)
        sys.exit(0)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
