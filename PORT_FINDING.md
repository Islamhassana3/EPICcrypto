# Port Finding Feature

## Overview

EPICcrypto now includes automatic port availability checking to prevent conflicts with other services running on your system. This feature ensures that the application never tries to use a port that's already in use, providing a seamless startup experience.

## How It Works

### Automatic Port Detection

When you start the application (via `app.py` or any of the preview scripts), it will:

1. **Check the preferred port** (default: 5000, or from `PORT` environment variable)
2. **If available**, use that port
3. **If occupied**, automatically find the next available port (5001, 5002, etc.)
4. **Display clear messages** about which port is being used

### Example Output

**When port 5000 is available:**
```
==================================================
🎉 Starting EPICcrypto...
==================================================

🌐 The application will open automatically in your browser
📍 URL: http://localhost:5000
```

**When port 5000 is occupied:**
```
🔍 Checking port availability...
⚠️  Port 5000 is already in use
✅ Using alternative port: 5001

==================================================
🎉 Starting EPICcrypto...
==================================================

🌐 The application will open automatically in your browser
📍 URL: http://localhost:5001
```

## Usage

### Running Directly with Python

```bash
python app.py
```

The app will automatically find an available port and display the URL.

### Using Preview Scripts

All preview scripts now include automatic port finding:

**Linux/macOS:**
```bash
./preview.sh
```

**Windows PowerShell:**
```powershell
.\preview.ps1
```

**Windows Command Prompt:**
```cmd
preview.bat
```

### Custom Port Selection

You can still specify a custom port using the `PORT` environment variable:

**Linux/macOS:**
```bash
export PORT=8000
python app.py
```

**Windows PowerShell:**
```powershell
$env:PORT = "8000"
python app.py
```

**Windows Command Prompt:**
```cmd
set PORT=8000
python app.py
```

**Using .env file:**
```bash
echo "PORT=8000" > .env
python app.py
```

Even with a custom port, the application will find an alternative if that port is occupied.

## Technical Details

### Port Finder Module

The core functionality is in `backend/utils/port_finder.py`:

- **`is_port_available(port, host='0.0.0.0')`**: Check if a specific port is available
- **`find_available_port(preferred_port=5000, host='0.0.0.0', max_attempts=10)`**: Find an available port

### Helper Script

`find_port.py` is a simple script used by shell scripts to determine available ports:

```bash
python3 find_port.py 5000
# Output: 5000 (or next available port)
```

### Integration in app.py

The main application (`app.py`) uses the port finder automatically:

```python
if __name__ == '__main__':
    preferred_port = int(os.environ.get('PORT', 5000))
    port = find_available_port(preferred_port)
    
    if port != preferred_port:
        logger.warning(f"Port {preferred_port} was not available. Using port {port} instead.")
        print(f"\n⚠️  Port {preferred_port} is already in use.")
        print(f"✅ Starting server on alternative port: {port}")
        print(f"🌐 Access the application at: http://localhost:{port}\n")
    
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True')
```

## Benefits

1. **No More Port Conflicts**: Never override existing services
2. **Automatic Fallback**: No manual intervention needed
3. **Clear Communication**: Always know which port is being used
4. **Development-Friendly**: Run multiple instances for testing
5. **Production-Ready**: Works seamlessly in all environments

## Testing

The feature includes comprehensive test coverage:

- **Unit tests**: `tests/test_port_finder.py`
- **Integration tests**: `tests/test_integration_port.py`

Run tests with:
```bash
python3 tests/test_port_finder.py
python3 tests/test_integration_port.py
```

## Troubleshooting

### Port Range Exhausted

If the first 10 ports starting from your preferred port are all occupied, you'll see an error:

```
RuntimeError: Could not find an available port after checking 10 ports starting from 5000
```

**Solution**: Manually specify a port in a different range:
```bash
export PORT=8000
python app.py
```

### Permission Denied

If you see "Permission denied" on Linux/macOS when trying to use ports below 1024:

**Solution**: Either run as root (not recommended) or use a port >= 1024:
```bash
export PORT=8080
python app.py
```

### Scripts Can't Find Python

If the preview scripts can't find Python:

**Solution**: Ensure Python is in your PATH, or edit the scripts to use the full path to your Python executable.

## Future Enhancements

Possible future improvements:

- Configurable port range (e.g., search between 5000-5100)
- Port preference file to remember last used port
- Option to reserve specific ports
- Support for binding to specific network interfaces

## Contributing

Found a bug or have a suggestion? Please open an issue on GitHub!
