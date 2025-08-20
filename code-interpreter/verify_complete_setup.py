#!/usr/bin/env python3

import requests
import json
import os
import sys
from pathlib import Path

def verify_setup():
    \"\"\"Comprehensive verification of the Code Interpreter Service setup\"\"\"
    
    print(\"🔍 Comprehensive Code Interpreter Service Verification\")
    print(\"=\" * 60)
    
    # 1. Check directory structure
    print(\"\n📁 1. Checking directory structure...\")
    required_dirs = [
        \"services/code-interpreter\",
        \"services/code-interpreter/src\",
        \"services/code-interpreter/config\"
    ]
    
    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if full_path.exists() and full_path.is_dir():
            print(f\"   ✅ {dir_path}\")
        else:
            print(f\"   ❌ {dir_path} (missing)\")
    
    # 2. Check required files
    print(\"\n📄 2. Checking required files...\")
    required_files = [
        \"services/code-interpreter/src/main.py\",
        \"services/code-interpreter/requirements.txt\",
        \"services/code-interpreter/Dockerfile\",
        \"services/code-interpreter/docker-compose.override.yml\",
        \"services/code-interpreter/README.md\"
    ]
    
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists() and full_path.is_file():
            print(f\"   ✅ {file_path}\")
        else:
            print(f\"   ❌ {file_path} (missing)\")
    
    # 3. Check environment variables
    print(\"\n⚙️  3. Checking environment configuration...\")
    
    # Check .env file
    env_file = Path(\".env\")
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
            
        required_vars = [
            \"LIBRECHAT_CODE_API_KEY\",
            \"CODE_BASEURL\"
        ]
        
        for var in required_vars:
            if var in env_content:
                print(f\"   ✅ {var} found in .env\")
            else:
                print(f\"   ❌ {var} missing from .env\")
    else:
        print(\"   ❌ .env file not found\")
    
    # 4. Check docker-compose.override.yml
    print(\"\n🐳 4. Checking Docker Compose configuration...\")
    override_file = Path(\"docker-compose.override.yml\")
    if override_file.exists():
        with open(override_file, 'r') as f:
            override_content = f.read()
            
        if \"code_interpreter\" in override_content:
            print(\"   ✅ code_interpreter service found in docker-compose.override.yml\")
        else:
            print(\"   ❌ code_interpreter service missing from docker-compose.override.yml\")
            
        if \"LIBRECHAT_CODE_API_KEY\" in override_content:
            print(\"   ✅ LIBRECHAT_CODE_API_KEY found in docker-compose.override.yml\")
        else:
            print(\"   ❌ LIBRECHAT_CODE_API_KEY missing from docker-compose.override.yml\")
    else:
        print(\"   ❌ docker-compose.override.yml file not found\")
    
    # 5. Test service connectivity (if running)
    print(\"\n🌐 5. Testing service connectivity...\")
    
    # Try to get the base URL from environment
    code_baseurl = os.getenv('CODE_BASEURL', 'http://localhost:8700')
    
    try:
        response = requests.get(f\"{code_baseurl}/v1/health\", timeout=5)
        if response.status_code == 200:
            print(f\"   ✅ Service is reachable at {code_baseurl}\")
            print(f\"   📊 Health status: {response.json()}\")
        else:
            print(f\"   ❌ Service returned status code: {response.status_code}\")
    except requests.exceptions.ConnectionError:
        print(f\"   ⚠️  Service not reachable at {code_baseurl} (may not be running)\")
    except requests.exceptions.Timeout:
        print(f\"   ❌ Timeout connecting to service at {code_baseurl}\")
    except Exception as e:
        print(f\"   ❌ Error connecting to service: {e}\")
    
    # 6. Summary
    print(\"\n📋 Summary:\")
    print(\"   To start the complete system:\")
    print(\"   1. Run: ./start_with_code_interpreter.sh\")
    print(\"   2. Access LibreChat at: http://localhost:3080\")
    print(\"   3. Code Interpreter API at: http://localhost:8700\")
    print(\"\")
    print(\"   To test the service directly:\")
    print(\"   python services/code-interpreter/test_service.py\")

if __name__ == \"__main__\":
    verify_setup()