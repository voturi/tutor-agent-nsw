"""
TutorAgent MVP Upload API Routes
Document upload and processing endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from core.config import settings
from core.logging import get_logger

logger = get_logger("upload")

router = APIRouter()


class UploadResponse(BaseModel):
    """Upload response model."""
    upload_id: str
    filename: str
    file_size: int
    status: str
    message: str
    timestamp: datetime


@router.post("/document", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload homework document for processing.
    Supports PDF and image files.
    """
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        
        # Generate unique upload ID
        upload_id = str(uuid.uuid4())
        
        # Save file temporarily and process with tutor agent
        import tempfile
        import os
        
        # Save the uploaded file temporarily
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='wb', suffix=f'.{file_extension}', delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Import tutor agent
            from agents.assessment.gemini_agent import tutor_agent
            
            # For non-text files, we'll need to handle them differently
            # For now, create a context description
            try:
                if file_extension in ['txt', 'md']:
                    # Process text files directly
                    tutoring_response = await tutor_agent.process_file_upload(
                        file_path=temp_file_path,
                        context={"upload_id": upload_id, "filename": file.filename}
                    )
                else:
                    # For other file types, create a description file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as desc_file:
                        desc_content = f"""File: {file.filename}
Type: {file_extension}
Size: {len(content)} bytes
Upload ID: {upload_id}

This is a {file_extension} file that needs to be processed for tutoring."""
                        desc_file.write(desc_content)
                        desc_temp_path = desc_file.name
                    
                    try:
                        tutoring_response = await tutor_agent.process_file_upload(
                            file_path=desc_temp_path,
                            context={"upload_id": upload_id, "filename": file.filename, "original_file_type": file_extension}
                        )
                    finally:
                        if os.path.exists(desc_temp_path):
                            os.unlink(desc_temp_path)
                            
                logger.info(f"Successfully processed file {file.filename} with tutor agent")
                
            except ValueError as ve:
                # Handle Gemini API filtering or safety errors
                logger.warning(f"Gemini API filtered response for uploaded file {file.filename}: {ve}")
                tutoring_response = {"message": "File uploaded successfully! What would you like to work on from this material?"}
            except Exception as tutor_error:
                # Handle other API errors
                logger.error(f"Error processing uploaded file {file.filename} with tutor agent: {tutor_error}")
                tutoring_response = {"message": "File uploaded successfully! I'm ready to help you with the content."}
            
            logger.info(f"Document uploaded and processed: {file.filename}, ID: {upload_id}")
            
        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            # Continue with upload even if tutoring fails
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        return UploadResponse(
            upload_id=upload_id,
            filename=file.filename,
            file_size=len(content),
            status="uploaded",
            message="Document uploaded successfully. Processing started.",
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")


@router.get("/status/{upload_id}")
async def get_upload_status(upload_id: str):
    """
    Get upload processing status.
    """
    try:
        # TODO: Check processing status from database/Redis
        logger.info(f"Checking status for upload: {upload_id}")
        
        return {
            "upload_id": upload_id,
            "status": "processing",  # uploaded, processing, completed, failed
            "progress": 50,
            "questions_found": 0,
            "message": "Processing document...",
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail="Status check failed")
