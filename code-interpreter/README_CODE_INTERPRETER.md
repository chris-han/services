# LibreChat with Code Interpreter Service

This repository contains the complete LibreChat application enhanced with a Code Interpreter Service that provides secure sandboxed code execution capabilities.

## 🚀 Quick Start

To start LibreChat with the Code Interpreter Service:

```bash
# Make the startup script executable
chmod +x start_with_code_interpreter.sh

# Start the complete system
./start_with_code_interpreter.sh
```

Then access:
- **LibreChat**: http://localhost:3080
- **Code Interpreter API**: http://localhost:8700

## 📁 Project Structure

```
├── api/                    # Main LibreChat API
├── client/                 # Frontend application
├── packages/               # Shared packages
├── services/               
│   └── code-interpreter/   # Code Interpreter Service (NEW)
├── docker-compose.yml      # Main Docker Compose configuration
├── docker-compose.override.yml  # Service overrides
├── .env                    # Environment configuration
└── start_with_code_interpreter.sh  # Startup script
```

## 🔧 Code Interpreter Service

The Code Interpreter Service provides a secure sandbox environment for executing code in multiple programming languages:

### Supported Languages
- Python (`py`)
- JavaScript (`js`)
- TypeScript (`ts`)
- C (`c`)
- C++ (`cpp`)
- Java (`java`)
- PHP (`php`)
- Go (`go`)
- Rust (`rs`)
- D (`d`)
- Fortran90 (`f90`)
- R (`r`)

### Key Features
- ✅ Multi-language code execution
- ✅ File upload and management
- ✅ Session-based file persistence
- ✅ API key authentication
- ✅ Secure sandboxed execution
- ✅ Automatic generated file delivery
- ✅ RESTful API compliant with LibreChat specifications

## 🐳 Docker Deployment

The service is fully containerized and can be deployed using Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🛠️ Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Code Interpreter Service
LIBRECHAT_CODE_API_KEY=your-code-api-key-here
CODE_BASEURL=http://code_interpreter:8700
```

### Docker Compose Override

The `docker-compose.override.yml` file includes the Code Interpreter service configuration:

```yaml
services:
  code_interpreter:
    build:
      context: ./services/code-interpreter
      dockerfile: Dockerfile
    ports:
      - "8700:8700"
    environment:
      - CODE_API_KEY=your-code-api-key-here
      - PORT=8700
```

## 🔍 API Endpoints

### Execute Code
```
POST /v1/exec
```
Execute code in a specified language with optional arguments and file references.

### Upload Files
```
POST /v1/upload
```
Upload files to be used during code execution.

### Get Files Information
```
GET /v1/files/{session_id}
```
Retrieve information about files associated with a session.

### Delete a File
```
DELETE /v1/files/{session_id}/{file_id}
```
Delete a specific file from a session.

### Download a File
```
GET /v1/download/{session_id}/{file_id}
```
Download a generated file from a session.

### Health Check
```
GET /v1/health
```
Check the health status of the service.

## 🔒 Security

The service implements several security measures:
- API key authentication for all endpoints
- 30-second execution timeout to prevent infinite loops
- 100MB file size limit
- Sandboxed execution environment
- Session-based file isolation

## 🧪 Testing

Run the automated test suite:

```bash
# Test the service
python services/code-interpreter/test_service.py

# Example usage
python services/code-interpreter/example_usage.py
```

## 📚 Documentation

Detailed documentation is available in the `services/code-interpreter/` directory:

- [`README.md`](services/code-interpreter/README.md) - Service overview
- [`USAGE.md`](services/code-interpreter/USAGE.md) - API usage guide
- [`DEVELOPMENT.md`](services/code-interpreter/DEVELOPMENT.md) - Development guide
- [`SUMMARY.md`](services/code-interpreter/SUMMARY.md) - Implementation summary

## 🆘 Troubleshooting

### Common Issues

1. **Permission denied errors**: Ensure Docker has proper file permissions
2. **Language support issues**: Verify all required language runtimes are installed
3. **Connection refused**: Check that services are running on the correct ports
4. **Authentication failures**: Verify API keys match between configuration files

### Debugging

Check Docker logs:
```bash
docker logs code_interpreter
```

Enable verbose logging:
```bash
export LOG_LEVEL=DEBUG
```

## 🤝 Contributing

Contributions are welcome! Please see the [Development Guide](services/code-interpreter/DEVELOPMENT.md) for information on setting up a development environment and contributing guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LibreChat](https://librechat.ai) - The main application this service enhances
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used for the service
- All the language runtime maintainers and communities