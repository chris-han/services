from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Query, Form, Header
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import os
import uuid
import subprocess
import tempfile
import shutil
import hashlib
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LibreChat Code Interpreter API",
    description="API for sandbox code execution and file management",
    version="1.0.0"
)

# Configuration
UPLOAD_DIR = "/tmp/code-exec/uploads"
EXECUTION_DIR = "/tmp/code-exec/sessions"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
API_KEY = os.getenv("CODE_API_KEY", "default-api-key")

# Create directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXECUTION_DIR, exist_ok=True)

logger.info(f"Code Interpreter Service starting with API_KEY: {API_KEY[:5]}...")

# Models
class FileRef(BaseModel):
    id: str
    name: str
    path: str

class RequestFile(BaseModel):
    id: str
    session_id: str
    name: str

class ExecuteResponse(BaseModel):
    run: Dict[str, Any]
    language: str
    version: str
    session_id: str
    files: List[FileRef]

class RequestBody(BaseModel):
    code: str = Field(..., description="The source code to be executed")
    lang: str = Field(..., description="The programming language of the code", example="py")
    args: Optional[str] = Field(None, description="Optional command line arguments to pass to the program")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    entity_id: Optional[str] = Field(None, description="Optional assistant/agent identifier for file sharing and reference. Must be a valid nanoid-compatible string.", example="asst_axIyVEqAa3UVppsVP3WTl5So")
    files: Optional[List[RequestFile]] = Field(None, description="Array of file references to be used during execution")

class FileObject(BaseModel):
    name: str
    id: str
    session_id: str
    content: Optional[str] = None
    size: Optional[int] = None
    lastModified: Optional[str] = None
    etag: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    contentType: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    session_id: str
    files: List[FileObject]

class Error(BaseModel):
    error: str
    details: Optional[str] = None

# Security
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return x_api_key

# Helper functions
def get_file_info(file_path: str) -> dict:
    try:
        stat = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat.st_size,
            "lastModified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "etag": hashlib.md5(str(stat.st_mtime).encode()).hexdigest()
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {e}")
        return {}

def cleanup_execution_dir(session_dir: str):
    try:
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir, ignore_errors=True)
    except Exception as e:
        logger.error(f"Error cleaning up execution directory {session_dir}: {e}")

# Endpoints
@app.post("/exec", response_model=ExecuteResponse, responses={401: {"model": Error}, 503: {"model": Error}})
async def execute_code(body: RequestBody, api_key: str = Depends(verify_api_key)):
    logger.info(f"Executing code in language: {body.lang}")
    
    try:
        code = body.code
        lang = body.lang
        args = body.args or []
        user_id = body.user_id
        entity_id = body.entity_id
        files = body.files or []
        
        if not code or not lang:
            raise HTTPException(status_code=400, detail="Missing required parameters: code and lang")
        
        # Generate session ID
        session_id = entity_id or str(uuid.uuid4())
        session_dir = os.path.join(EXECUTION_DIR, session_id)
        
        # Create session directory
        os.makedirs(session_dir, exist_ok=True)
        
        # Copy uploaded files to session directory
        for file_ref in files:
            source_path = os.path.join(UPLOAD_DIR, file_ref.name)
            dest_path = os.path.join(session_dir, file_ref.name)
            
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
        
        # Write code to file
        file_ext = ""
        if lang == "py":
            file_ext = ".py"
        elif lang == "js":
            file_ext = ".js"
        elif lang == "ts":
            file_ext = ".ts"
        elif lang == "c":
            file_ext = ".c"
        elif lang == "cpp":
            file_ext = ".cpp"
        elif lang == "java":
            file_ext = ".java"
        elif lang == "php":
            file_ext = ".php"
        elif lang == "rs":
            file_ext = ".rs"
        elif lang == "go":
            file_ext = ".go"
        elif lang == "d":
            file_ext = ".d"
        elif lang == "f90":
            file_ext = ".f90"
        elif lang == "r":
            file_ext = ".R"
        else:
            file_ext = ".txt"
        
        code_filename = f"code{file_ext}"
        code_filepath = os.path.join(session_dir, code_filename)
        
        with open(code_filepath, "w") as f:
            f.write(code)
        
        # Prepare execution command based on language
        command = ""
        timeout = 30  # 30 seconds
        
        if lang == "py":
            command = f"cd {session_dir} && python3 {code_filename}"
        elif lang == "js":
            command = f"cd {session_dir} && node {code_filename}"
        elif lang == "ts":
            # First compile TypeScript, then run
            command = f"cd {session_dir} && npx tsc {code_filename} && node {code_filename.replace('.ts', '.js')}"
        elif lang == "c":
            command = f"cd {session_dir} && gcc {code_filename} -o program && ./program"
        elif lang == "cpp":
            command = f"cd {session_dir} && g++ {code_filename} -o program && ./program"
        elif lang == "java":
            command = f"cd {session_dir} && javac {code_filename} && java {code_filename.replace('.java', '')}"
        elif lang == "php":
            command = f"cd {session_dir} && php {code_filename}"
        elif lang == "go":
            command = f"cd {session_dir} && go run {code_filename}"
        elif lang == "r":
            command = f"cd {session_dir} && Rscript {code_filename}"
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")
        
        # Add arguments if provided
        if args:
            command += f" {args}"
        
        # Execute code
        logger.info(f"Executing command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=session_dir
            )
            stdout = result.stdout
            stderr = result.stderr
            code_result = result.returncode
            signal = None
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout.decode() if e.stdout else ""
            stderr = (e.stderr.decode() if e.stderr else "") + "\nExecution timed out"
            code_result = 1
            signal = "SIGTERM"
        except Exception as e:
            stdout = ""
            stderr = str(e)
            code_result = 1
            signal = None
        
        # Get generated files
        generated_files = []
        for file in os.listdir(session_dir):
            if file != code_filename:
                file_path = os.path.join(session_dir, file)
                if os.path.isfile(file_path):
                    generated_files.append(FileRef(
                        id=str(uuid.uuid4()),
                        name=file,
                        path=f"/download/{session_id}/{file}"
                    ))
        
        # Prepare response
        response = ExecuteResponse(
            run={
                "stdout": stdout,
                "stderr": stderr,
                "code": code_result,
                "signal": signal,
                "output": stdout,
                "message": None,
                "status": None,
                "cpu_time": None,
                "wall_time": None
            },
            language=lang,
            version="1.0.0",
            session_id=session_id,
            files=generated_files
        )
        
        logger.info(f"Code execution completed with exit code: {code_result}")
        return response
    except Exception as e:
        logger.error(f"Error during code execution: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/upload", response_model=UploadResponse, responses={413: {"model": Error}})
async def upload_files(
    files: List[UploadFile] = File(...),
    entity_id: Optional[str] = Form(None),
    api_key: str = Depends(verify_api_key)
):
    logger.info(f"Uploading {len(files)} files")
    
    try:
        session_id = entity_id or str(uuid.uuid4())
        session_dir = os.path.join(EXECUTION_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        uploaded_files = []
        
        for file in files:
            # Check file size
            contents = await file.read()
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File size limit exceeded")
            
            # Reset file pointer
            await file.seek(0)
            
            # Save file
            file_path = os.path.join(session_dir, file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            
            # Get file info
            file_info = get_file_info(file_path)
            if file_info:
                uploaded_files.append(FileObject(
                    name=file.filename,
                    id=str(uuid.uuid4()),
                    session_id=session_id,
                    content=None,  # We don't include content in the response for security
                    size=file_info.get("size"),
                    lastModified=file_info.get("lastModified"),
                    etag=file_info.get("etag"),
                    metadata={
                        "content-type": file.content_type,
                        "original-filename": file.filename
                    },
                    contentType=file.content_type
                ))
        
        logger.info(f"Successfully uploaded {len(uploaded_files)} files")
        return UploadResponse(
            message="Files uploaded successfully",
            session_id=session_id,
            files=uploaded_files
        )
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/files/{session_id}", response_model=List[FileObject])
async def get_files(
    session_id: str,
    detail: str = Query("simple"),
    api_key: str = Depends(verify_api_key)
):
    logger.info(f"Getting files for session: {session_id}")
    
    try:
        session_dir = os.path.join(EXECUTION_DIR, session_id)
        
        if not os.path.exists(session_dir):
            raise HTTPException(status_code=404, detail="Session not found")
        
        files = []
        for file in os.listdir(session_dir):
            file_path = os.path.join(session_dir, file)
            if os.path.isfile(file_path):
                file_obj = FileObject(
                    name=file,
                    id=str(uuid.uuid4()),
                    session_id=session_id
                )
                
                if detail == "full":
                    file_info = get_file_info(file_path)
                    file_obj.content = None  # We don't include content for security
                    file_obj.size = file_info.get("size")
                    file_obj.lastModified = file_info.get("lastModified")
                    file_obj.etag = file_info.get("etag")
                    file_obj.metadata = {
                        "content-type": "application/octet-stream",
                        "original-filename": file
                    }
                    file_obj.contentType = "application/octet-stream"
                
                files.append(file_obj)
        
        logger.info(f"Found {len(files)} files for session: {session_id}")
        return files
    except Exception as e:
        logger.error(f"Error getting files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/files/{session_id}/{file_id}", responses={500: {"model": Error}})
async def delete_file(
    session_id: str,
    file_id: str,
    api_key: str = Depends(verify_api_key)
):
    logger.info(f"Deleting file: {file_id} from session: {session_id}")
    
    try:
        # In a real implementation, we would map file_id to actual filename
        # For this example, we'll assume file_id is the filename
        file_path = os.path.join(EXECUTION_DIR, session_id, file_id)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        logger.info(f"Successfully deleted file: {file_id}")
        return {"message": "File deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/download/{session_id}/{file_id}")
async def download_file(
    session_id: str,
    file_id: str,
    api_key: str = Depends(verify_api_key)
):
    logger.info(f"Downloading file: {file_id} from session: {session_id}")
    
    try:
        # In a real implementation, we would map file_id to actual filename
        # For this example, we'll assume file_id is the filename
        file_path = os.path.join(EXECUTION_DIR, session_id, file_id)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    logger.info("Starting Code Interpreter Service on port 8700")
    uvicorn.run(app, host="0.0.0.0", port=8700)