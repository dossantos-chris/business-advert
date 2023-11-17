from bson.objectid import ObjectId

from app.server.db import db

business_collection = db.businesses

def business_helper(business) -> dict:
    result = {
        "_id": str(business["_id"]),
        "name": business["name"],
        "service": business["service"],
        "city": business["city"],
        "state": business["state"],
        "dateAdded": business["dateAdded"]
    }

    if "lastUpdated" in business:
        result["lastUpdated"] = business["lastUpdated"]

    return result

async def retrieve_businesses() -> list[dict]:
    businesses = []
    async for business in business_collection.find():
        businesses.append(business_helper(business))
    return(businesses)

async def retrieve_business(id: str) -> dict:
    business = await business_collection.find_one({"_id": ObjectId(id)})
    if business:
        return business_helper(business)

async def add_business(business_data: dict) -> dict:
    business = await business_collection.insert_one(business_data)
    new_business = await business_collection.find_one({"_id": business.inserted_id})
    return business_helper(new_business)

async def update_business(id: str, data: dict) -> bool:
    if len(data) < 1:
        return False
    business = await business_collection.find_one({"_id": ObjectId(id)})
    if business:
        updated_business = await business_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_business:
            return True
    return False

async def delete_business(id: str) -> bool:
    business = await business_collection.find_one({"_id": ObjectId(id)})
    if business:
        await business_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
