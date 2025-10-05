@echo off
REM EPICcrypto Quick Preview Launch Script
REM For Windows systems (Command Prompt)
REM
REM This script automatically:
REM - Checks if Python is installed
REM - Checks if dependencies are installed
REM - Installs missing dependencies
REM - Starts the development server
REM - Opens the application in your default browser

echo ==================================================
echo    EPICcrypto Quick Preview Launcher
echo ==================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed!
    echo Please install Python 3.11 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Check if virtual environment exists
echo Checking virtual environment...
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies (this may take a minute)...
    python -m pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
    echo    Verifying all packages...
    pip install -q -r requirements.txt
)
echo.

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] Creating .env file from .env.example...
        copy .env.example .env >nul
        echo [OK] .env file created
    ) else (
        echo [WARNING] No .env file found (optional)
    )
    echo.
)

REM Get the port (default to 5000) and find an available one
if "%PORT%"=="" set PREFERRED_PORT=5000
if not "%PORT%"=="" set PREFERRED_PORT=%PORT%

echo Checking port availability...
for /f %%i in ('python find_port.py %PREFERRED_PORT% 2^>nul') do set AVAILABLE_PORT=%%i

if "%AVAILABLE_PORT%"=="" (
    echo [ERROR] Could not find an available port
    pause
    exit /b 1
)

if not "%AVAILABLE_PORT%"=="%PREFERRED_PORT%" (
    echo [WARNING] Port %PREFERRED_PORT% is already in use
    echo [OK] Using alternative port: %AVAILABLE_PORT%
) else (
    echo [OK] Port %AVAILABLE_PORT% is available
)
echo.

set PORT=%AVAILABLE_PORT%

echo ==================================================
echo    Starting EPICcrypto...
echo ==================================================
echo.
echo The application will open automatically in your browser
echo URL: http://localhost:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo.

REM Wait a moment before opening browser
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:%PORT%

REM Start the Flask application
python app.py
