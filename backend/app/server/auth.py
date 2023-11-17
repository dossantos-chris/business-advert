from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.server.models.user import (
    UserSchema,
    UserInDBSchema,
    Token,
    TokenData
)

from app.server.models.response import (
    ErrorResponseModel,
    ResponseModel
)

SECRET_KEY = "4f159fb87443de7b9435aeb74f7f446c9d830367d777b48f14b6abe4c8e9e855"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_db = {
    "chris": {
        "username": "chris",
        "hashed_password": "",
        "disabled": False
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDBSchema(**user_data)
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = JSONResponse(content = ErrorResponseModel("An error occured.", 401, "Could not validate credentials",),
                                        staus_code = 401,
                                        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token)
        username : str = payload.get("sub")
        if username is None:
            return credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        return credential_exception
    
    user = get_user(fake_db, username=token_data.username)
    if user is None:
        return credential_exception
    
    return user
