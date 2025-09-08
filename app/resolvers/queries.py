import strawberry
from typing import Optional
from strawberry.types import Info
from app.schemas.user import UserType
from app.schemas.email import EmailType, EmailListType
from app.schemas.statistics import StatisticsType
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.auth import verify_token

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
class Query:
    @strawberry.field
    def get_user(self, info: Info) -> UserType:
        """Get current user data"""
        user_id = get_current_user(info)
        db = info.context["db"]
        
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise Exception("User not found")
        
        return user_service.to_user_type(user)
    
    @strawberry.field
    def get_statistics(self, info: Info) -> StatisticsType:
        """Get email statistics for current user"""
        user_id = get_current_user(info)
        db = info.context["db"]
        
        email_service = EmailService(db)
        stats = email_service.get_statistics(user_id)
        
        if not stats:
            # Return empty statistics if none exist
            return StatisticsType(
                id=0,
                total=0,
                productive=0,
                unproductive=0,
                percentage_productive=0.0,
                percentage_unproductive=0.0
            )
        
        # Calculate percentages
        total = stats.total
        percentage_productive = (stats.productive / total * 100) if total > 0 else 0.0
        percentage_unproductive = (stats.unproductive / total * 100) if total > 0 else 0.0
        
        return StatisticsType(
            id=stats.id,
            total=stats.total,
            productive=stats.productive,
            unproductive=stats.unproductive,
            percentage_productive=round(percentage_productive, 2),
            percentage_unproductive=round(percentage_unproductive, 2)
        )
    
    @strawberry.field
    def get_emails_list(self, info: Info, page: int = 1, per_page: int = 10) -> EmailListType:
        """Get paginated list of emails for current user"""
        user_id = get_current_user(info)
        db = info.context["db"]
        
        email_service = EmailService(db)
        return email_service.get_emails_list(user_id, page, per_page)
    
    @strawberry.field
    def get_email(self, info: Info, email_id: int) -> EmailType:
        """Get specific email by ID for current user"""
        user_id = get_current_user(info)
        db = info.context["db"]
        
        email_service = EmailService(db)
        email = email_service.get_email_by_id(user_id, email_id)
        
        if not email:
            raise Exception("Email not found")
        
        return email_service.to_email_type(email)
