#
# EPICcrypto Quick Preview Launch Script
# For Windows PowerShell
#
# This script automatically:
# - Checks if Python is installed
# - Checks if dependencies are installed
# - Installs missing dependencies
# - Starts the development server
# - Opens the application in your default browser
#

# Enable error handling
$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   🚀 EPICcrypto Quick Preview Launcher" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.11 or higher from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check if virtual environment exists
Write-Host "🔍 Checking virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    & python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check if requirements are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
try {
    & python -c "import flask" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask not installed"
    }
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
    Write-Host "   Verifying all packages..." -ForegroundColor Gray
    & pip install -q -r requirements.txt
} catch {
    Write-Host "📦 Installing dependencies (this may take a minute)..." -ForegroundColor Yellow
    & python -m pip install -q --upgrade pip
    & pip install -q -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No .env file found (optional)" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Get the port (default to 5000) and find an available one
$PREFERRED_PORT = if ($env:PORT) { $env:PORT } else { "5000" }
Write-Host "🔍 Checking port availability..." -ForegroundColor Yellow

try {
    $AVAILABLE_PORT = & python find_port.py $PREFERRED_PORT
    if ($LASTEXITCODE -ne 0) {
        throw "Could not find available port"
    }
    
    if ($AVAILABLE_PORT -ne $PREFERRED_PORT) {
        Write-Host "⚠️  Port $PREFERRED_PORT is already in use" -ForegroundColor Yellow
        Write-Host "✅ Using alternative port: $AVAILABLE_PORT" -ForegroundColor Green
    } else {
        Write-Host "✅ Port $AVAILABLE_PORT is available" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Could not find an available port" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

$PORT = $AVAILABLE_PORT

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   🎉 Starting EPICcrypto..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 The application will open automatically in your browser" -ForegroundColor Green
Write-Host "📍 URL: http://localhost:$PORT" -ForegroundColor Green
Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Wait a moment before opening browser
Start-Sleep -Seconds 2

# Open browser
Start-Process "http://localhost:$PORT"

# Start the Flask application
& python app.py
