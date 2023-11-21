from pydantic import ConfigDict, BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    hashed_password: str = Field(...)
    disabled: bool | None = None
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "chris",
            "hashed_password": "Password1234",
            "disabled": False
        }
    })