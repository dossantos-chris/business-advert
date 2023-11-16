from fastapi import APIRouter

router = APIRouter()

from app.server.models.response import (
    ErrorResponseModel,
    ResponseModel
)

@router.get("/")
async def get_user_data():
    return ResponseModel({"test":"test"}, "This is a test")