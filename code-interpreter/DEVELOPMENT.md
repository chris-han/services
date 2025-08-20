# Code Interpreter Service Development Guide

## Local Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install language runtimes (if not using Docker):
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y gcc g++ openjdk-11-jdk nodejs npm r-base php-cli golang-go rustc
   sudo npm install -g typescript
   ```

3. Start the service locally:
   ```bash
   export CODE_API_KEY=your-secret-api-key
   python src/main.py
   ```

## Project Structure

```
services/code-interpreter/
├── src/                 # Source code
│   └── main.py         # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Production Docker image
├── Dockerfile.test      # Test Docker image
├── docker-compose.yml   # Docker Compose configuration
├── start.sh            # Service startup script
├── init.sh             # Initialization script
├── test_service.py     # Automated tests
├── example_usage.py    # Example usage demonstrations
├── README.md           # Service documentation
└── USAGE.md            # API usage guide
```

## Development Workflow

1. Make changes to the source code in `src/main.py`
2. Test locally using the test scripts:
   ```bash
   python test_service.py
   ```
3. Build and test Docker image:
   ```bash
   docker-compose -f docker-compose.test.yml up --build
   ```
4. Run integration tests:
   ```bash
   docker-compose -f docker-compose.test.yml run code_interpreter_test
   ```

## API Development

The API follows the OpenAPI specification defined in `code-interpreter/openapi.json`. When making changes to endpoints, ensure they remain compatible with this specification.

## Testing

Run automated tests:
```bash
python test_service.py
```

This will test:
- Health check endpoint
- Code execution functionality
- Error handling
- Security (unauthorized access)

## Debugging

Enable verbose logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

Check Docker logs:
```bash
docker logs code_interpreter
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure nothing is broken
5. Submit a pull request

## Common Issues

### Permission Errors
Ensure the `/tmp/code-exec` directory has proper permissions:
```bash
sudo chown -R $(whoami) /tmp/code-exec
chmod -R 755 /tmp/code-exec
```

### Language Support Issues
Verify all required language runtimes are installed:
```bash
python --version
node --version
javac -version
# etc.
```

### Docker Build Failures
Clear Docker cache and rebuild:
```bash
docker builder prune
docker-compose build --no-cache
```