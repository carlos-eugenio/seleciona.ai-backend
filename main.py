from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from strawberry.fastapi import GraphQLRouter
from app.database import get_db, engine, Base
from app.resolvers import Query, Mutation
from app.routers import upload
from app.config import settings
from app.auth import verify_token
from app.services.email_service import EmailService
# Import models to register them with SQLAlchemy
from app.models import User, CategorizedEmail, EmailStatistics
import strawberry
import os
import tempfile
import shutil

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads directory
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/avatars", exist_ok=True)

# Create FastAPI app
app = FastAPI(title="Seleciona AI Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create GraphQL router with dependency injection
async def get_context(request: Request, db=Depends(get_db)):
    return {
        "db": db,
        "request": request
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

# Add GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

# Add upload endpoints
app.include_router(upload.router)

# GraphQL File Upload endpoint (works with Altair)
@app.post("/graphql/upload")
async def graphql_file_upload(
    file: UploadFile = File(...),
    authorization: str = None,
    db=Depends(get_db)
):
    """
    GraphQL-compatible file upload endpoint that works with Altair
    """
    try:
        # Get token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        token = authorization.split(" ")[1]
        token_data = verify_token(token)
        user_id = token_data["user_id"]
        
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
                "data": {
                    "analyseEmailsFromUpload": {
                        "success": True,
                        "message": f"Successfully processed {processed_count} emails",
                        "processedCount": processed_count,
                        "fileName": file.filename
                    }
                }
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

# Serve the upload demo HTML file
@app.get("/upload-demo")
async def upload_demo():
    """Serve the upload demo HTML page"""
    return FileResponse("upload_demo.html")

@app.get("/")
async def root():
    return {"message": "Seleciona AI Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
