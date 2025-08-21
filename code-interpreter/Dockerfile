# Use Ubuntu 22.04 as base for better package support
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    openjdk-11-jdk \
    nodejs \
    npm \
    r-base \
    php-cli \
    golang-go \
    rustc \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install additional language tools
RUN npm install -g typescript

# Create directories for execution with proper permissions
RUN mkdir -p /tmp/code-exec/uploads /tmp/code-exec/sessions && \
    chmod -R 777 /tmp/code-exec

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 8700

# Set environment variables
ENV PYTHONPATH=/app
ENV CODE_API_KEY=default-api-key

# Run the application
CMD ["python3", "src/main.py"]