#!/bin/bash

# Initialize Code Interpreter Service
echo "🔧 Initializing Code Interpreter Service..."

# Create necessary directories with proper permissions
mkdir -p /tmp/code-exec/uploads
mkdir -p /tmp/code-exec/sessions

# Set permissions
chmod 755 /tmp/code-exec
chmod 755 /tmp/code-exec/uploads
chmod 755 /tmp/code-exec/sessions

# Set ownership if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Setting ownership for directories..."
    # Use nobody user if available, otherwise keep root
    if id -u nobody >/dev/null 2>&1; then
        chown -R nobody:nogroup /tmp/code-exec
    fi
fi

echo "✅ Initialization complete!"
echo "Starting service with CODE_API_KEY: ${CODE_API_KEY:-default-api-key}"