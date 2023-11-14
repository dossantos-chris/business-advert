from flask import Flask, jsonify, request
from models import Business
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.BusinessAdvert
CORS(app) 

@app.route("/list", methods=["GET"])
async def list():
    businessCursor = db.businesses.find({})
    businesses = await businessCursor.to_list(None)

    for business in businesses:
        business['_id'] = str(business['_id'])

    return jsonify({"businesses": businesses}), 200

@app.route("/add", methods=["POST"])
async def add():
    data = request.json

    if 'name' in data and 'service' in data and 'city' in data and 'state' in data:
        new_business = Business(data['name'], data['service'], data['city'], data['state'])

        business_dict = vars(new_business)

        result = await db.businesses.insert_one(business_dict)

        if result.inserted_id:
            return jsonify({'message': 'Document created successfully.', '_id': str(result.inserted_id)}), 201
        else:
            return jsonify({'error': 'Failed to create document.'}), 500
    else:
        return jsonify({'error': 'Invalid business model'}), 400

@app.route("/delete", methods=['DELETE'])
async def delete():
    business_id = request.args.get('id', None)

    if business_id is None:
        return jsonify({"error": "Must include a business ID"}) , 400

    try:
        oid = ObjectId(business_id)
    except:
        return jsonify({"error": "Not a valid business ID"}) , 400

    result = await db.businesses.delete_one({"_id": oid})

    if result.deleted_count == 0:
        return jsonify({"error": "Business not found"}) , 404

    return jsonify({"message": "Business deleted successfully", '_id': business_id}), 200

if __name__ == "__main__":
    app.run(debug=True)