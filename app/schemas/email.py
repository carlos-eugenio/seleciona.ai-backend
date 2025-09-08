import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum

@strawberry.enum
class EmailClassification(Enum):
    PRODUCTIVE = "PRODUCTIVE"
    UNPRODUCTIVE = "UNPRODUCTIVE"

@strawberry.type
class EmailType:
    id: int
    user_id: int
    email: str
    subject: str
    response: str
    classification: EmailClassification
    created_at: datetime
    updated_at: datetime

@strawberry.input
class EmailInput:
    email: str
    subject: str
    message: str

@strawberry.input
class EmailUpdateInput:
    email_id: int
    response: str

@strawberry.type
class PaginationType:
    page: int
    per_page: int
    total: int
    total_pages: int

@strawberry.type
class EmailListType:
    emails: List[EmailType]
    pagination: PaginationType

# New types for file upload
@strawberry.type
class FileUploadResult:
    success: bool
    message: str
    processed_count: int
    file_name: Optional[str] = None

# GraphQL Upload scalar for file uploads
@strawberry.scalar
class Upload:
    def __init__(self, file):
        self.file = file
    
    @classmethod
    def serialize(cls, value):
        return value
    
    @classmethod
    def parse_value(cls, value):
        return value
    
    @classmethod
    def parse_literal(cls, value):
        return value