"""
Basic tests for EPICcrypto application
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test that core modules can be imported"""
    try:
        import app
        from services import crypto_data
        from services import ai_predictor
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_app_structure():
    """Test that Flask app has required routes"""
    try:
        import app as flask_app
        
        # Check that app exists
        assert hasattr(flask_app, 'app'), "Flask app not found"
        
        # Check basic configuration
        assert flask_app.app is not None, "Flask app is None"
        
        print("✓ App structure valid")
        return True
    except AssertionError as e:
        print(f"✗ App structure invalid: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking app structure: {e}")
        return False

def test_crypto_service():
    """Test CryptoDataService basic functionality"""
    try:
        from services.crypto_data import CryptoDataService
        
        service = CryptoDataService()
        assert service is not None, "Service not initialized"
        
        # Check that methods exist
        assert hasattr(service, 'get_historical_data'), "get_historical_data method missing"
        assert hasattr(service, 'calculate_technical_indicators'), "calculate_technical_indicators method missing"
        
        print("✓ CryptoDataService structure valid")
        return True
    except AssertionError as e:
        print(f"✗ CryptoDataService invalid: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing CryptoDataService: {e}")
        return False

def test_ai_predictor():
    """Test AIPredictor basic functionality"""
    try:
        from services.ai_predictor import AIPredictor
        
        predictor = AIPredictor()
        assert predictor is not None, "Predictor not initialized"
        
        # Check that methods exist
        assert hasattr(predictor, 'predict'), "predict method missing"
        assert hasattr(predictor, 'prepare_features'), "prepare_features method missing"
        
        print("✓ AIPredictor structure valid")
        return True
    except AssertionError as e:
        print(f"✗ AIPredictor invalid: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing AIPredictor: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'README.md',
        'services/__init__.py',
        'services/crypto_data.py',
        'services/ai_predictor.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files present")
        return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running EPICcrypto Basic Tests")
    print("="*50 + "\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("App Structure", test_app_structure),
        ("CryptoDataService", test_crypto_service),
        ("AIPredictor", test_ai_predictor),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 50)
        result = test_func()
        results.append((test_name, result))
    
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
