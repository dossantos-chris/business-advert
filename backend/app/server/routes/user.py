from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.server.database.user import (
    get_user
)

from app.server.models.user import (
    UserSchema
)

from app.server.models.response import (
    ErrorResponseModel,
    ResponseModel
)

SECRET_KEY = "4f159fb87443de7b9435aeb74f7f446c9d830367d777b48f14b6abe4c8e9e855"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    
async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
    except jwt.ExpiredSignatureError:
        return JSONResponse(content = ErrorResponseModel("An error occured", 401, "Token expired",),
                            status_code = 401,
                            headers = {"WWW-Authenticate": "Bearer"})
    except JWTError:
        return JSONResponse(content = ErrorResponseModel("An error occured", 401, "Could not validate credentials",),
                            status_code = 401,
                            headers = {"WWW-Authenticate": "Bearer"})
    
    user = await get_user(username)
    if not user:
        return JSONResponse(content = ErrorResponseModel("An error occured", 401, "User no longer exists",),
                            status_code = 404,
                            headers = {"WWW-Authenticate": "Bearer"})
    
    if user["disabled"]:
        return JSONResponse(content = ErrorResponseModel("An error occurred", 400, "Inactive user"),
                            status_code = 400)
    return user

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        return JSONResponse(content = ErrorResponseModel("An error occurred", 401, "Incorrect username or password"),
                            status_code = 401,
                            headers = {"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_current_user(current_user: UserSchema = Depends(get_current_user)):
    return current_user