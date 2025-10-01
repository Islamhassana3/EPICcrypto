#!/usr/bin/env python3
"""
Deployment verification script for EPICcrypto
Run this before deploying to ensure everything is ready
"""

import sys
import os

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False

def check_python_syntax(filepath):
    """Check Python file syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✓ Valid syntax: {filepath}")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {filepath}: {e}")
        return False

def main():
    """Main verification function"""
    print("="*60)
    print("EPICcrypto Deployment Verification")
    print("="*60)
    print()
    
    checks = []
    
    # Check required files
    print("Checking required files...")
    checks.append(check_file_exists("app.py", "Main application"))
    checks.append(check_file_exists("requirements.txt", "Dependencies"))
    checks.append(check_file_exists("Procfile", "Start command"))
    checks.append(check_file_exists("runtime.txt", "Python version"))
    checks.append(check_file_exists("railway.json", "Railway config"))
    checks.append(check_file_exists("nixpacks.toml", "Build config"))
    checks.append(check_file_exists("services/crypto_data.py", "Data service"))
    checks.append(check_file_exists("services/ai_predictor.py", "AI predictor"))
    checks.append(check_file_exists("templates/index.html", "UI template"))
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    checks.append(check_python_syntax("app.py"))
    checks.append(check_python_syntax("services/crypto_data.py"))
    checks.append(check_python_syntax("services/ai_predictor.py"))
    if os.path.exists("config.py"):
        checks.append(check_python_syntax("config.py"))
    print()
    
    # Check configuration
    print("Checking configuration...")
    with open("Procfile", "r") as f:
        procfile = f.read()
        if "gunicorn" in procfile and "app:app" in procfile:
            print("✓ Procfile configured correctly")
            checks.append(True)
        else:
            print("✗ Procfile may have issues")
            checks.append(False)
    
    with open("runtime.txt", "r") as f:
        runtime = f.read().strip()
        if runtime.startswith("python-3.1"):
            print(f"✓ Python version: {runtime}")
            checks.append(True)
        else:
            print(f"✗ Unusual Python version: {runtime}")
            checks.append(False)
    print()
    
    # Summary
    print("="*60)
    passed = sum(checks)
    total = len(checks)
    print(f"Verification Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ All checks passed! Ready for deployment.")
        print("="*60)
        print()
        print("Next steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Deploy on Railway.app")
        print("3. Follow RAILWAY_DEPLOYMENT.md for detailed instructions")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
