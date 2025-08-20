#!/usr/bin/env python3

import subprocess
import sys
import os
import signal
import time

class CodeInterpreterService:
    def __init__(self):
        self.process = None
    
    def start_service(self):
        \"\"\"Start the code interpreter service locally\"\"\"
        print(\"🚀 Starting Code Interpreter Service...\")
        
        # Change to the service directory
        service_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(service_dir)
        
        # Set environment variables
        os.environ['CODE_API_KEY'] = os.getenv('LIBRECHAT_CODE_API_KEY', 'your-code-api-key-here')
        os.environ['PYTHONPATH'] = '/app'
        
        try:
            # Start the FastAPI service
            self.process = subprocess.Popen([
                sys.executable, 'src/main.py'
            ])
            
            print(f\"✅ Service started with PID: {self.process.pid}\")
            print(\"📍 Service available at: http://localhost:8700\")
            print(\"🔐 API Key: your-code-api-key-here\")
            print(\"💡 Press Ctrl+C to stop the service\")
            
            # Wait for the process
            self.process.wait()
            
        except KeyboardInterrupt:
            print(\"\\n🛑 Stopping service...\")
            self.stop_service()
        except Exception as e:
            print(f\"❌ Error starting service: {e}\")
            self.stop_service()
    
    def stop_service(self):
        \"\"\"Stop the code interpreter service\"\"\"
        if self.process:
            try:
                # Terminate the process
                self.process.terminate()
                self.process.wait(timeout=5)
                print(\"✅ Service stopped successfully\")
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                self.process.kill()
                self.process.wait()
                print(\"⚠️  Service force killed\")
            except Exception as e:
                print(f\"❌ Error stopping service: {e}\")
        else:
            print(\"ℹ️  Service is not running\")

def main():
    print(\"🔧 Code Interpreter Service Manager\")
    print(\"=\" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == \"stop\":
        service = CodeInterpreterService()
        service.stop_service()
        return
    
    # Start the service
    service = CodeInterpreterService()
    try:
        service.start_service()
    except KeyboardInterrupt:
        print(\"\\n👋 Goodbye!\")

if __name__ == \"__main__\":
    main()