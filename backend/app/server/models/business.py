from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, Union, List

class BusinessSchema(BaseModel):
    name: str = Field(...)
    service: Union[str, List[str]] = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    dateAdded : str = str(datetime.utcnow())

    class Config:
        schema_extra = {
            "example": {
                "name": "Aqua Blue",
                "service": ["bar", "restaurant"],
                "city": "Toms River",
                "state": "New Jersey",
                "dateAdded": "2023-11-14 16:04:56.209516",
            }
        }

class UpdateBusinessSchema(BaseModel):
    name: Optional[str] = None
    service: Optional[Union[str, List[str]]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    lastUpdated: str = str(datetime.utcnow())

    class Config:
        schema_extra = {
            "example": {
                "city": "Seaside",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}