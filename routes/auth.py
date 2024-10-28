from fastapi import Body, status, HTTPException, Depends, APIRouter, Response
from models import User
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import schemas, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserCreate):
    """
    A route with POST method to Create a New User account.
    """
    # Hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    new_user = User(**user.dict())
    
    # Creates a new user 
    await new_user.insert() 

    return {"message":"User Successfully Created"}


@router.post('/signin', response_model=schemas.Token)
async def sign_in(user_credentials:OAuth2PasswordRequestForm=Depends()):
    """
    A route with POST method to Sign in to a User account.

    """

    user = await User.find_one(User.email == user_credentials.username)

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid email or password")
    
    access_token = oauth2.create_access_token(data = {"user_id": str(user.id)}) 
    refresh_token = oauth2.refresh_access_token(data = {"user_id": str(user.id)}) 

    return {"access_token": access_token, "refresh_token": refresh_token, "message": "Token Generated" }


@router.post('/refresh', response_model=schemas.Token)
async def refresh(refresh_token_model: schemas.RefreshToken = Body()):
    """
    A route with POST method to provid a refresh token
    
    """

    user_id = oauth2.verify_access_token(refresh_token_model.refresh_token)
    access_token = oauth2.create_access_token(data = {"user_id": str(user_id)}) 

    return {"access_token": access_token, "refresh_token": refresh_token_model.refresh_token, "message": "new Token Generated" }


     



