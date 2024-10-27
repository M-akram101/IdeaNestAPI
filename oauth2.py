from fastapi import Depends, HTTPException,status
import jwt
from jose import JWTError
from datetime import datetime, timedelta
from models import User
from fastapi.security import OAuth2PasswordBearer
from config import settings
import database, models, schemas
#secret_key


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_access_token_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)


    return encoded_access_token_jwt


def refresh_access_token(data: dict):
        to_encode = data.copy()
        expire_refresh= datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire_refresh})
        encoded_refresh_token_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
        return encoded_refresh_token_jwt


def verify_access_token(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers = {"www-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return id

#take token from request automatically, extract id for us
#its going to verify that the token is correct by calling verify access token
#can be passed to any path we have as a dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_access_token(token)
    user = await User.get(user_id)
    return user
