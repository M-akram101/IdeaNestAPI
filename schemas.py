from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from models import AccessLevel
 
# User Requests Schema 
# For the signup

class User(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True 

class UserOrganization(BaseModel):
    name: str
    email:str
    access_level: AccessLevel
# For the user signup
class UserCreate(User):
    name: str
    
#For the user login
class UserLogin(User):
    pass

# For the inviting a user to an organization
class UserInvite(BaseModel):
    user_email: str
# For the refresh token
class TokenRefreshRequest(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    message: str


class RefreshToken(BaseModel):
    refresh_token: str


# Organization Requests Schema
# For creating Organization
class Organization(BaseModel):
    
    name: str
    description: str
    # created_by: int
    class Config:
        orm_mode = True 

#For Organization Update
class OrganizationUpdate(Organization):
    pass

class OrganizationWithUsers(Organization):
    organization_members: List = []

# For User Invitation
class Invitation(Organization):
    pass




## general classes

class ResponseOut(BaseModel):
    message: str
