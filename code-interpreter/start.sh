#!/bin/bash

# Startup script for Code Interpreter Service

echo "🚀 Starting Code Interpreter Service..."

# Run initialization
./init.sh

# Set environment variables
export PYTHONPATH=/app
export CODE_API_KEY=${CODE_API_KEY:-default-api-key}

# Start the service
echo "▶️ Starting FastAPI server..."
python src/main.py