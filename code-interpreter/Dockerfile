# Use official uv image with Python 3.13 as base
FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    openjdk-17-jdk \
    nodejs \
    r-base \
    php-cli \
    golang-go \
    rustc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install bun for Node.js package management
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Install additional language tools
RUN bun add -g typescript

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