#!/bin/bash

# Startup script for LibreChat with Code Interpreter Service

echo "🚀 Starting LibreChat with Code Interpreter Service..."
echo "======================================================"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found!"
    echo "   Please run this script from the LibreChat root directory."
    exit 1
fi

# Check if docker-compose.override.yml exists
if [ ! -f "docker-compose.override.yml" ]; then
    echo "⚠️  Warning: docker-compose.override.yml not found!"
    echo "   Creating a default override file..."
    
    cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  code_interpreter:
    build:
      context: ./services/code-interpreter
      dockerfile: Dockerfile
    container_name: code_interpreter
    ports:
      - "8700:8700"
    environment:
      - CODE_API_KEY=your-code-api-key-here
      - PORT=8700
    volumes:
      - ./services/code-interpreter/data:/tmp/code-exec
    restart: always

  api:
    environment:
      - LIBRECHAT_CODE_API_KEY=your-code-api-key-here
      - CODE_BASEURL=http://code_interpreter:8700
EOF

    echo "✅ Created default docker-compose.override.yml"
fi

# Check if .env file has the required variables
if ! grep -q "LIBRECHAT_CODE_API_KEY" .env 2>/dev/null; then
    echo "⚠️  Warning: LIBRECHAT_CODE_API_KEY not found in .env!"
    echo "   Adding to .env file..."
    
    echo "" >> .env
    echo "#====================================#" >> .env
    echo "# LibreChat Code Interpreter API     #" >> .env
    echo "#====================================#" >> .env
    echo "" >> .env
    echo "LIBRECHAT_CODE_API_KEY=your-code-api-key-here" >> .env
    echo "CODE_BASEURL=http://localhost:8700" >> .env
    
    echo "✅ Added Code Interpreter configuration to .env"
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo "✅ Services started successfully!"
    echo ""
    echo "📘 Access your services at:"
    echo "   LibreChat: http://localhost:3080"
    echo "   Code Interpreter API: http://localhost:8700"
    echo ""
    echo "🔧 To view logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 To stop services:"
    echo "   docker-compose down"
else
    echo "❌ Error starting services!"
    echo "   Check the logs with: docker-compose logs"
fi