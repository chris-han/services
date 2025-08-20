# LibreChat Code Interpreter Service

## Overview

The Code Interpreter Service provides a secure sandbox environment for executing code in multiple programming languages. It's designed to work with the LibreChat platform as part of its code execution capabilities.

## Quick Start

1. **Build and start the service:**
   ```bash
   docker-compose up --build
   ```

2. **Test the service:**
   ```bash
   # Run the test suite
   python services/code-interpreter/test_service.py
   ```

## API Endpoints

### Execute Code (`/exec`)

Execute code in a specified language.

**Method:** `POST`
**Headers:**
- `Content-Type: application/json`
- `x-api-key: your-api-key`

**Request Body:**
```json
{
  "code": "print('Hello, World!')",
  "lang": "py",
  "args": "--verbose"
}
```

**Supported Languages:**
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

### Upload Files (`/upload`)

Upload files to be used during code execution.

**Method:** `POST`
**Headers:**
- `x-api-key: your-api-key`

**Form Data:**
- `files`: One or more file uploads
- `entity_id`: Optional session identifier

### Get Files (`/files/{session_id}`)

Retrieve information about files in a session.

**Method:** `GET`
**Headers:**
- `x-api-key: your-api-key`

### Delete File (`/files/{session_id}/{file_id}`)

Delete a specific file from a session.

**Method:** `DELETE`
**Headers:**
- `x-api-key: your-api-key`

### Download File (`/download/{session_id}/{file_id}`)

Download a generated file from a session.

**Method:** `GET`
**Headers:**
- `x-api-key: your-api-key`

### Health Check (`/health`)

Check the health status of the service.

**Method:** `GET`

## Environment Variables

- `CODE_API_KEY`: API key for authenticating requests (default: "default-api-key")
- `PORT`: Port to run the service on (default: 8700)

## Security

The service uses API key authentication for all endpoints. Make sure to:
1. Set a strong `CODE_API_KEY` in your environment
2. Keep the API key secret and don't expose it in client-side code
3. Use HTTPS in production environments

## Language Support

Each language runs in an isolated environment with specific tools installed:

| Language | Runtime |
|----------|---------|
| Python | Python 3.11 |
| JavaScript | Node.js |
| TypeScript | TypeScript compiler + Node.js |
| C | GCC |
| C++ | G++ |
| Java | OpenJDK 11 |
| PHP | PHP CLI |
| Go | Go compiler |
| Rust | Rust compiler |
| D | D compiler |
| Fortran90 | GFortran |
| R | R |

## Best Practices

1. **Always handle errors gracefully** - Code execution can fail for various reasons
2. **Set reasonable timeouts** - The service has a 30-second execution timeout
3. **Validate inputs** - Sanitize any user-provided code before execution
4. **Limit resource usage** - The service has built-in limits on file sizes and execution time
5. **Handle file operations carefully** - Generated files are automatically delivered to users

## Troubleshooting

### Service won't start
- Check that all required environment variables are set
- Verify Docker has sufficient resources allocated
- Check logs for specific error messages

### Code execution fails
- Verify the language is supported
- Check that the code is syntactically correct
- Ensure file paths are relative to the execution directory
- Check that the code doesn't exceed resource limits

### Authentication errors
- Verify the `x-api-key` header is set correctly
- Check that the API key matches the `CODE_API_KEY` environment variable
- Ensure there are no extra spaces or characters in the API key

## Integration with LibreChat

To integrate with LibreChat:

1. Set the `LIBRECHAT_CODE_API_KEY` environment variable in your LibreChat configuration
2. Set the `CODE_BASEURL` to point to your code interpreter service (e.g., `http://code_interpreter:8700`)
3. Restart LibreChat to pick up the new configuration

The service will automatically be available in the LibreChat interface when users have the proper permissions.