from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DEACTIVE = "DEACTIVE"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE, index=True)
    avatar_url = Column(String(500), nullable=True)
    avatar_thumbnail_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    categorized_emails = relationship("CategorizedEmail", back_populates="user")
    email_statistics = relationship("EmailStatistics", back_populates="user")
