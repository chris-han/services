#!/usr/bin/env python3

import requests
import sys

def health_check():
    try:
        response = requests.get("http://localhost:8700/v1/health", timeout=5)
        if response.status_code == 200:
            print("Health check: OK")
            return True
        else:
            print(f"Health check failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check failed with error: {e}")
        return False

if __name__ == "__main__":
    if health_check():
        sys.exit(0)
    else:
        sys.exit(1)