from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel,Field
from beanie import Document, Indexed, Link

class AccessLevel(str, Enum):
    admin = "admin"
    member = "member"
    guest = "guest"



class Organization(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., example="The name of the organization")
    description: str = Field(..., example="A brief description of the organization")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "organizations" 

    class Config:
        arbitrary_types_allowed = True 
        schema_extra = {
            "example": {
                "_id": "64b8c6a4567890abcd123456", 
                "name": "Egyptian organization",
                "description": "An organization focused on saas",
                "created_at": datetime.now().isoformat(),
            }
        }


class User(Document):
    id: UUID = Field(default_factory=uuid4)    
    name: str = Field(..., example="Enter Your Full Name")
    email: str = Indexed(unique=True)
    password: str = Field(..., example="Enter Your Full Name")
    access_level: AccessLevel = Field(default=AccessLevel.member)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    organization_id: Optional[UUID]  

    
    class Settings:
        name = "users"

    class Config:
        arbitrary_types_allowed = True 
        schema_extra={
            "example": {
                "name": "Mohamed Akram",
                "email": "m.akram@gmail.com",
                "password": "mypassword1234",
                "access_level": "member",
                "created_at": datetime.now().isoformat(),
            }
        }

