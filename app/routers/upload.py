from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from app.services.email_service import EmailService
import os
import tempfile
import shutil
from typing import List

router = APIRouter(prefix="/api/upload", tags=["upload"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Get current user ID from token"""
    token = credentials.credentials
    token_data = verify_token(token)
    return token_data["user_id"]

@router.post("/emails", response_model=dict)
async def upload_emails_file(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Upload and process emails from a file.
    Supports .txt and .pdf files.
    Expected format: email|subject|message (one per line)
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.txt', '.pdf']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be .txt or .pdf"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            # Copy uploaded file to temporary file
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        try:
            # Process the temporary file
            email_service = EmailService(db)
            emails_data = _process_file(temp_file_path)
            
            # Process each email
            processed_count = 0
            for email_data in emails_data:
                email_service.create_email(
                    user_id=user_id,
                    email=email_data['email'],
                    subject=email_data['subject'],
                    message=email_data['message']
                )
                processed_count += 1
            
            return {
                "success": True,
                "message": f"Successfully processed {processed_count} emails",
                "processed_count": processed_count,
                "file_name": file.filename
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

@router.post("/emails/multiple", response_model=dict)
async def upload_multiple_emails_files(
    files: List[UploadFile] = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Upload and process emails from multiple files.
    Supports .txt and .pdf files.
    Expected format: email|subject|message (one per line)
    """
    try:
        if not files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No files provided"
            )
        
        email_service = EmailService(db)
        total_processed = 0
        results = []
        
        for file in files:
            try:
                # Validate file type
                if not file.filename:
                    results.append({
                        "file_name": "unknown",
                        "success": False,
                        "message": "No filename provided",
                        "processed_count": 0
                    })
                    continue
                
                file_extension = os.path.splitext(file.filename)[1].lower()
                if file_extension not in ['.txt', '.pdf']:
                    results.append({
                        "file_name": file.filename,
                        "success": False,
                        "message": "File must be .txt or .pdf",
                        "processed_count": 0
                    })
                    continue
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    shutil.copyfileobj(file.file, temp_file)
                    temp_file_path = temp_file.name
                
                try:
                    # Process the temporary file
                    emails_data = _process_file(temp_file_path)
                    
                    # Process each email
                    processed_count = 0
                    for email_data in emails_data:
                        email_service.create_email(
                            user_id=user_id,
                            email=email_data['email'],
                            subject=email_data['subject'],
                            message=email_data['message']
                        )
                        processed_count += 1
                    
                    total_processed += processed_count
                    results.append({
                        "file_name": file.filename,
                        "success": True,
                        "message": f"Successfully processed {processed_count} emails",
                        "processed_count": processed_count
                    })
                    
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                        
            except Exception as e:
                results.append({
                    "file_name": file.filename if file.filename else "unknown",
                    "success": False,
                    "message": f"Error processing file: {str(e)}",
                    "processed_count": 0
                })
        
        return {
            "success": True,
            "message": f"Processed {len(files)} files, total emails: {total_processed}",
            "total_processed": total_processed,
            "files_processed": len([r for r in results if r["success"]]),
            "files_failed": len([r for r in results if not r["success"]]),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing files: {str(e)}"
        )

def _process_file(file_path: str) -> list:
    """Process file and extract email data"""
    emails_data = []
    
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple parsing - assuming format: email|subject|message
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip():  # Skip empty lines
                        parts = line.split('|', 2)
                        if len(parts) == 3:
                            emails_data.append({
                                'email': parts[0].strip(),
                                'subject': parts[1].strip(),
                                'message': parts[2].strip()
                            })
        
        elif file_path.endswith('.pdf'):
            # For PDF processing, you would use PyPDF2 or similar
            # This is a simplified version
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Simple parsing for PDF
                lines = text.strip().split('\n')
                for line in lines:
                    if line.strip():  # Skip empty lines
                        parts = line.split('|', 2)
                        if len(parts) == 3:
                            emails_data.append({
                                'email': parts[0].strip(),
                                'subject': parts[1].strip(),
                                'message': parts[2].strip()
                            })
    
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")
    
    return emails_data