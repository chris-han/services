#!/usr/bin/env python3

import requests
import json
import time

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get("http://localhost:8700/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            return True
        else:
            print(f"❌ Health check: FAILED (Status code: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health check: FAILED (Error: {e})")
        return False

def test_python_execution():
    """Test Python code execution"""
    print("\nTesting Python code execution...")
    url = "http://localhost:8700/exec"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "your-code-api-key-here"
    }
    
    data = {
        "code": "print('Hello, World!')\nprint('This is a test of the code interpreter service.')",
        "lang": "py"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Python execution: PASSED")
            print(f"   Output: {result['run'].get('stdout', '').strip()}")
            return True
        else:
            print(f"❌ Python execution: FAILED (Status code: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Python execution: FAILED (Error: {e})")
        return False

def test_error_handling():
    """Test error handling with invalid code"""
    print("\nTesting error handling...")
    url = "http://localhost:8700/exec"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "your-code-api-key-here"
    }
    
    data = {
        "code": "invalid_syntax_error",
        "lang": "py"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            # Even with errors, we expect a successful response with error info
            print("✅ Error handling: PASSED")
            if result['run'].get('stderr'):
                print(f"   Error captured: {result['run'].get('stderr', '').strip()[:100]}...")
            return True
        else:
            print(f"❌ Error handling: FAILED (Status code: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error handling: FAILED (Error: {e})")
        return False

def test_unauthorized_access():
    """Test unauthorized access"""
    print("\nTesting unauthorized access...")
    url = "http://localhost:8700/exec"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "wrong-api-key"
    }
    
    data = {
        "code": "print('test')",
        "lang": "py"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 401:
            print("✅ Unauthorized access: PASSED (Correctly rejected)")
            return True
        else:
            print(f"❌ Unauthorized access: FAILED (Expected 401, got {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Unauthorized access: FAILED (Error: {e})")
        return False

def main():
    print("=" * 50)
    print("Code Interpreter Service Test Suite")
    print("=" * 50)
    
    # Wait a moment for service to start
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_python_execution,
        test_error_handling,
        test_unauthorized_access
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)