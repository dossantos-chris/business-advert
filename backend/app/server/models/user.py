from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    disabled: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "Chris",
                "password": "Password1234",
                "disabled": False
            }
        }

class UserInDBSchema(UserSchema):
    hashed_password: str = Field(...)

class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)

class TokenData(BaseModel):
    username: str | None = None