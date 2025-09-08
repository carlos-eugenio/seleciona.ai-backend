import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum
from strawberry.types import Info
from app.schemas.auth import LoginInput, LoginResponse
from app.schemas.user import UserType, UserInput, UserUpdateInput
from app.schemas.email import EmailType, EmailInput, EmailUpdateInput, FileUploadResult, Upload
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.auth import verify_token, create_access_token
from app.models.user import UserStatus
from app.schemas.email import EmailClassification
import os
import tempfile
import shutil
from app.config import settings

def get_current_user(info: Info) -> int:
    """Get current user ID from token"""
    # Extract token from request headers
    request = info.context.get("request")
    if not request:
        raise Exception("Request not available")
    
    # Get token from Authorization header
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Authentication required")
    
    token = auth_header.split(" ")[1]
    token_data = verify_token(token)
    return token_data["user_id"]

@strawberry.type
class Mutation:
    @strawberry.field
    def login(self, info: Info, input: LoginInput) -> LoginResponse:
        """Login user and return token"""
        db = info.context["db"]
        user_service = UserService(db)
        
        user = user_service.authenticate_user(input.email, input.password)
        if not user:
            raise Exception("Invalid email or password")
        
        if user.status != UserStatus.ACTIVE:
            raise Exception("User account is deactivated")
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return LoginResponse(
            token=access_token,
            user=user_service.to_user_type(user)
        )
    
    @strawberry.field
    def create_user_account(self, info: Info, input: UserInput) -> UserType:
        """Create new user account (public endpoint)"""
        db = info.context["db"]
        user_service = UserService(db)
        
        # Check if email already exists
        existing_user = user_service.get_user_by_email(input.email)
        if existing_user:
            raise Exception("Email already registered")
        
        # Create new user
        user = user_service.create_user(input.name, input.email, input.password)
        return user_service.to_user_type(user)
    
    @strawberry.field
    def update_user_account(self, info: Info, input: UserUpdateInput) -> UserType:
        """Update current user account"""
        user_id = get_current_user(info)
        db = info.context["db"]
        user_service = UserService(db)
        
        # Check if email is being changed and if it already exists
        if input.email:
            existing_user = user_service.get_user_by_email(input.email)
            if existing_user and existing_user.id != user_id:
                raise Exception("Email already registered")
        
        user = user_service.update_user(
            user_id, 
            name=input.name, 
            email=input.email, 
            password=input.password
        )
        
        if not user:
            raise Exception("User not found")
        
        return user_service.to_user_type(user)
    
    @strawberry.field
    def analyse_email(self, info: Info, input: EmailInput) -> EmailType:
        """Analyze and categorize a single email"""
        user_id = get_current_user(info)
        db = info.context["db"]
        email_service = EmailService(db)
        
        # Create and categorize the email
        email = email_service.create_email(
            user_id=user_id,
            email=input.email,
            subject=input.subject,
            message=input.message
        )
        
        return email_service.to_email_type(email)
    
    @strawberry.field
    def update_email(self, info: Info, input: EmailUpdateInput) -> EmailType:
        """Update email response"""
        user_id = get_current_user(info)
        db = info.context["db"]
        email_service = EmailService(db)
        
        email = email_service.update_email_response(
            user_id=user_id,
            email_id=input.email_id,
            response=input.response
        )
        
        if not email:
            raise Exception("Email not found")
        
        return email_service.to_email_type(email)
    
    @strawberry.field
    def delete_email(self, info: Info, email_id: int) -> bool:
        """Delete an email"""
        user_id = get_current_user(info)
        db = info.context["db"]
        email_service = EmailService(db)
        
        success = email_service.delete_email(user_id=user_id, email_id=email_id)
        
        if not success:
            raise Exception("Email not found")
        
        return True
    
    @strawberry.field
    def analyse_emails(self, info: Info, file_path: str) -> str:
        """Analyze multiple emails from file (legacy method)"""
        user_id = get_current_user(info)
        db = info.context["db"]
        email_service = EmailService(db)
        
        try:
            # Check file extension
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension not in ['.txt', '.pdf']:
                raise Exception("File must be .txt or .pdf")
            
            # Read and process file
            emails_data = self._process_file(file_path)
            
            # Process each email
            for email_data in emails_data:
                email_service.create_email(
                    user_id=user_id,
                    email=email_data['email'],
                    subject=email_data['subject'],
                    message=email_data['message']
                )
            
            return "Emails processed successfully"
            
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def _process_file(self, file_path: str) -> list:
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
