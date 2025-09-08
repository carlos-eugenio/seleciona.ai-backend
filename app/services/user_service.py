from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, UserStatus
from app.auth import verify_password, get_password_hash
from app.schemas.user import UserType
from typing import Optional
import os
from PIL import Image
import uuid

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.password):
            return user
        return None
    
    def create_user(self, name: str, email: str, password: str) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(password)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            status=UserStatus.ACTIVE
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user_id: int, name: Optional[str] = None, 
                   email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = get_password_hash(password)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def process_avatar(self, file_content: bytes, filename: str) -> tuple[str, str]:
        """Process and save avatar image"""
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/avatars"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save original image
        original_path = os.path.join(upload_dir, unique_filename)
        with open(original_path, "wb") as f:
            f.write(file_content)
        
        # Create thumbnail
        thumbnail_filename = f"thumb_{unique_filename}"
        thumbnail_path = os.path.join(upload_dir, thumbnail_filename)
        
        try:
            with Image.open(original_path) as img:
                # Resize to thumbnail (150x150)
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                img.save(thumbnail_path, "JPEG", quality=85)
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            # If thumbnail creation fails, use original as thumbnail
            thumbnail_path = original_path
        
        return original_path, thumbnail_path
    
    def update_user_avatar(self, user_id: int, file_content: bytes, filename: str) -> Optional[User]:
        """Update user avatar"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Process avatar
        avatar_path, thumbnail_path = self.process_avatar(file_content, filename)
        
        # Update user with new avatar URLs
        user.avatar_url = f"/{avatar_path}"
        user.avatar_thumbnail_url = f"/{thumbnail_path}"
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def to_user_type(self, user: User) -> UserType:
        """Convert User model to UserType schema"""
        return UserType(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar_url=user.avatar_url,
            avatar_thumbnail_url=user.avatar_thumbnail_url
        )
