from datetime import datetime
import os

from asgiref.wsgi import WsgiToAsgi
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn

from models import Business

app = Flask(__name__)
CORS(app) 
load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.BusinessAdvert

@app.route("/list", methods=["GET"])
async def list():
    businessCursor = db.businesses.find({})
    businesses = await businessCursor.to_list(None)

    for business in businesses:
        business["_id"] = str(business["_id"])

    return jsonify({"businesses": businesses}), 200

@app.route("/add", methods=["POST"])
async def add():
    data = request.get_json(force=True)

    if "name" in data and "service" in data and "city" in data and "state" in data:
        new_business = Business(data["name"], data["service"], data["city"], data["state"])

        business_dict = vars(new_business)

        result = await db.businesses.insert_one(business_dict)

        if result.inserted_id:
            return jsonify({"message": "Business created successfully.", "_id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Failed to create business"}), 500
    else:
        return jsonify({"error": "Invalid business model"}), 400

@app.route("/edit", methods=["POST"])
async def edit():
    business_id = request.args.get("id", None)

    if business_id is None:
        return jsonify({"error": "Must include a business ID"}) , 400

    try:
        oid = ObjectId(business_id)
    except:
        return jsonify({"error": "Not a valid business ID"}) , 400

    data = request.get_json(force=True)

    if "name" in data and "service" in data and "city" in data and "state" in data:
        new_business = Business(data["name"], data["service"], data["city"], data["state"])

        business_dict = vars(new_business)
        business_dict.pop("dateAdded")
        business_dict['lastUpdated'] = str(datetime.utcnow())

        result = await db.businesses.update_one({"_id": oid}, {"$set": business_dict})

        if result.modified_count == 0:
            return jsonify({"error": "Business not found"}), 404
        else:
            return jsonify({"message": "Business updated successfully", "_id": business_id}), 200
    else:
        return jsonify({"error": "Invalid business model"}), 400
    
@app.route("/delete", methods=["DELETE"])
async def delete():
    business_id = request.args.get("id", None)

    if business_id is None:
        return jsonify({"error": "Must include a business ID"}) , 400

    try:
        oid = ObjectId(business_id)
    except:
        return jsonify({"error": "Not a valid business ID"}) , 400

    result = await db.businesses.delete_one({"_id": oid})

    if result.deleted_count == 0:
        return jsonify({"error": "Business not found"}) , 404

    return jsonify({"message": "Business deleted successfully", "_id": business_id}), 200

if __name__ == "__main__":
    asgi_app = WsgiToAsgi(app)
    uvicorn.run(asgi_app, host="127.0.0.1", port=5000)