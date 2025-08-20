#!/usr/bin/env python3

import requests
import json
import os

def verify_service_configuration():
    """Verify that the code interpreter service is properly configured"""
    
    print("🔍 Verifying Code Interpreter Service Configuration...")
    print("=" * 50)
    
    # Check environment variables
    code_api_key = os.getenv('LIBRECHAT_CODE_API_KEY')
    code_baseurl = os.getenv('CODE_BASEURL')
    
    print(f"LIBRECHAT_CODE_API_KEY: {'✅ Set' if code_api_key else '❌ Not set'}")
    print(f"CODE_BASEURL: {code_baseurl if code_baseurl else '❌ Not set'}")
    
    if not code_api_key:
        print("\n⚠️  Warning: LIBRECHAT_CODE_API_KEY is not set in .env file")
        print("   Please set it to match the CODE_API_KEY in your docker-compose.override.yml")
    
    if not code_baseurl:
        print("\n⚠️  Warning: CODE_BASEURL is not set in .env file")
        print("   Please set it to point to your code interpreter service")
        print("   For local development: http://localhost:8700")
        print("   For Docker: http://code_interpreter:8700")
    
    # Test connection to service if URL is provided
    if code_baseurl:
        try:
            print(f"\n📡 Testing connection to {code_baseurl}...")
            response = requests.get(f"{code_baseurl}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Service is reachable")
                print(f"   Status: {response.json()}")
            else:
                print(f"❌ Service returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n📋 Configuration Summary:")
    print("   - Make sure CODE_API_KEY in docker-compose.override.yml matches LIBRECHAT_CODE_API_KEY in .env")
    print("   - Ensure CODE_BASEURL in .env points to the correct service URL")
    print("   - For Docker deployments, use http://code_interpreter:8700")
    print("   - For local development, use http://localhost:8700")

if __name__ == "__main__":
    verify_service_configuration()