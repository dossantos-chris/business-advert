from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.server.database.business import (
    retrieve_businesses,
    retrieve_business,
    add_business,
    update_business,
    delete_business
)

from app.server.models.business import (
    BusinessSchema,
    UpdateBusinessSchema
)

from app.server.models.response import (
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()

@router.get("/", response_description = "Businesses retrieved")
async def get_businesses():
    businesses = await retrieve_businesses()
    if businesses:
        return ResponseModel(businesses, "Business data retrieved successfully")
    return ResponseModel(businesses, "No businesses in the DB")

@router.get("/{id}", response_description = "Business data retrieved")
async def get_business_data(id: str):
    if len(id) != 24:
        return JSONResponse(content = ErrorResponseModel("An error occurred", 400, "Business ID must be length of 24"),
                        status_code = 400)

    business = await retrieve_business(id)
    if business:
        return ResponseModel(business, "Business data retrieved successfully")
    return JSONResponse(content = ErrorResponseModel("An error occurred", 404, "Business doesn't exist"),
                        status_code = 404)

@router.post("/", response_description = "Business data added into the database")
async def add_business_data(business: BusinessSchema = Body(...)):
    business = jsonable_encoder(business)
    new_business = await add_business(business)
    return ResponseModel(new_business, "Business added successfully")

@router.put("/{id}", response_description = "Business data updated")
async def update_business_data(id: str, req: UpdateBusinessSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_business = await update_business(id, req)
    if updated_business:
        return ResponseModel (
            f"Business with ID: {id} update is successful",
            "Business updated successfully",
        )
    return JSONResponse(content = ErrorResponseModel("An error occurred", 404 ,"There was an error updating the business data"),
                        status_code = 404)

@router.delete("/{id}", response_description = "Business data deleted from the database")
async def delete_business_data(id: str):
    deleted_business = await delete_business(id)
    if deleted_business:
        return ResponseModel(
            f"Business with ID: {id} removed", "Business deleted successfully"
        )
    return JSONResponse(content = ErrorResponseModel("An error occurred", 404, f"Business with id {id} doesn't exist"),
                        status_code = 404)
