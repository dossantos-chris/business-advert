from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    hashed_password: str = Field(...)
    disabled: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "chris",
                "hashed_password": "Password1234",
                "disabled": False
            }
        }

class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)

class TokenData(BaseModel):
    username: str | None = None