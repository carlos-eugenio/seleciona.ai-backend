from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.models.categorized_email import CategorizedEmail, EmailClassification
from app.models.email_statistics import EmailStatistics
from app.schemas.email import EmailType, EmailListType, PaginationType
from app.services.email_classifier import email_classifier
from typing import Optional, List, Tuple
import math

class EmailService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_email(self, user_id: int, email: str, subject: str, message: str) -> CategorizedEmail:
        """Create a new categorized email"""
        # Classify the email
        classification, response = email_classifier.classify_email(subject, message)
        
        # Create the email record
        categorized_email = CategorizedEmail(
            user_id=user_id,
            email=email,
            subject=subject,
            response=response,
            classification=EmailClassification(classification)
        )
        
        self.db.add(categorized_email)
        self.db.commit()
        self.db.refresh(categorized_email)
        
        # Update statistics
        self._update_statistics(user_id)
        
        return categorized_email
    
    def get_email_by_id(self, user_id: int, email_id: int) -> Optional[CategorizedEmail]:
        """Get email by ID for a specific user"""
        return self.db.query(CategorizedEmail).filter(
            and_(
                CategorizedEmail.id == email_id,
                CategorizedEmail.user_id == user_id
            )
        ).first()
    
    def get_emails_list(self, user_id: int, page: int = 1, per_page: int = 10) -> EmailListType:
        """Get paginated list of emails for a user"""
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get total count
        total = self.db.query(CategorizedEmail).filter(
            CategorizedEmail.user_id == user_id
        ).count()
        
        # Get emails with pagination
        emails = self.db.query(CategorizedEmail).filter(
            CategorizedEmail.user_id == user_id
        ).order_by(desc(CategorizedEmail.created_at)).offset(offset).limit(per_page).all()
        
        # Convert to EmailType
        email_types = [self.to_email_type(email) for email in emails]
        
        # Calculate pagination info
        total_pages = math.ceil(total / per_page) if total > 0 else 1
        
        pagination = PaginationType(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages
        )
        
        return EmailListType(
            emails=email_types,
            pagination=pagination
        )
    
    def update_email_response(self, user_id: int, email_id: int, response: str) -> Optional[CategorizedEmail]:
        """Update email response"""
        email = self.get_email_by_id(user_id, email_id)
        if not email:
            return None
        
        email.response = response
        self.db.commit()
        self.db.refresh(email)
        
        return email
    
    def delete_email(self, user_id: int, email_id: int) -> bool:
        """Delete an email"""
        email = self.get_email_by_id(user_id, email_id)
        if not email:
            return False
        
        self.db.delete(email)
        self.db.commit()
        
        # Update statistics
        self._update_statistics(user_id)
        
        return True
    
    def get_statistics(self, user_id: int) -> Optional[EmailStatistics]:
        """Get email statistics for a user"""
        return self.db.query(EmailStatistics).filter(
            EmailStatistics.user_id == user_id
        ).first()
    
    def _update_statistics(self, user_id: int):
        """Update or create email statistics for a user"""
        # Get current counts
        total = self.db.query(CategorizedEmail).filter(
            CategorizedEmail.user_id == user_id
        ).count()
        
        productive = self.db.query(CategorizedEmail).filter(
            and_(
                CategorizedEmail.user_id == user_id,
                CategorizedEmail.classification == EmailClassification.PRODUCTIVE
            )
        ).count()
        
        unproductive = self.db.query(CategorizedEmail).filter(
            and_(
                CategorizedEmail.user_id == user_id,
                CategorizedEmail.classification == EmailClassification.UNPRODUCTIVE
            )
        ).count()
        
        # Get or create statistics record
        stats = self.get_statistics(user_id)
        if not stats:
            stats = EmailStatistics(
                user_id=user_id,
                total=total,
                productive=productive,
                unproductive=unproductive
            )
            self.db.add(stats)
        else:
            stats.total = total
            stats.productive = productive
            stats.unproductive = unproductive
        
        self.db.commit()
        self.db.refresh(stats)
    
    def to_email_type(self, email: CategorizedEmail) -> EmailType:
        """Convert CategorizedEmail model to EmailType schema"""
        return EmailType(
            id=email.id,
            user_id=email.user_id,
            email=email.email,
            subject=email.subject,
            response=email.response,
            classification=email.classification,
            created_at=email.created_at,
            updated_at=email.updated_at
        )
