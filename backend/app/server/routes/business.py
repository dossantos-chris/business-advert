from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_businesses,
    retrieve_business,
    add_business,
    update_business,
    delete_business
)

from app.server.models.business import (
    ErrorResponseModel,
    ResponseModel,
    BusinessSchema,
    UpdateBusinessSchema,
)

router = APIRouter()

@router.get("/")
async def get_businesses():
    businesses = await retrieve_businesses()
    if businesses:
        return ResponseModel(businesses, "Business data retrieved successfully")
    return ResponseModel(businesses, "No businesses in the DB")

@router.get("/{id}")
async def get_business_data(id):
    business = await retrieve_business(id)
    if business:
        return ResponseModel(business, "Business data retrieved successfully")
    raise HTTPException(
        status_code = 404,
        detail = ErrorResponseModel("An error occurred.", 404, "Business doesn't exist.")
    )

@router.post("/")
async def add_business_data(business: BusinessSchema = Body(...)):
    business = jsonable_encoder(business)
    new_business = await add_business(business)
    return ResponseModel(new_business, "Business added successfully.")

@router.put("/{id}")
async def update_business_data(id: str, req: UpdateBusinessSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_business = await update_business(id, req)
    if updated_business:
        return ResponseModel (
            f"Business with ID: {id} update is successful",
            "Business updated successfully",
        )
    raise HTTPException(
        status_code = 404,
        detail = ErrorResponseModel("An error occurred", 404 ,"There was an error updating the business data.")
    )

@router.delete("/{id}")
async def delete_business_data(id: str):
    deleted_business = await delete_business(id)
    if deleted_business:
        return ResponseModel(
            f"Business with ID: {id} removed", "Business deleted successfully"
        )
    raise HTTPException(
        status_code = 404,
        detail = ErrorResponseModel("An error occurred", 404, f"Business with id {id} doesn't exist")
    )

