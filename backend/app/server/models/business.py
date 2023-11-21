from datetime import datetime

from pydantic import ConfigDict, BaseModel, Field, validator
from typing import Optional, List

class BusinessSchema(BaseModel):
    name: str = Field(...)
    service: str | List[str] = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    dateAdded : str = str(datetime.utcnow())
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Aqua Blue",
            "service": ["bar", "restaurant"],
            "city": "Toms River",
            "state": "New Jersey",
            "dateAdded": "2023-11-14 16:04:56.209516",
        }
    })

class UpdateBusinessSchema(BaseModel):
    name: Optional[str] = None
    service: Optional[str | List[str]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    lastUpdated: Optional[str] = None

    @validator("lastUpdated", pre=True, always=True)
    def set_last_updated(cls, last_updated, values):
        if any(values.get(field) for field in values if field != "lastUpdated"):
            return str(datetime.utcnow())
        return last_updated
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "city": "Seaside",
        }
    })