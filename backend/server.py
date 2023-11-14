from flask import Flask, jsonify, request
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
    return "test", 200

@app.route("/delete", methods=['DELETE'])
async def delete():
    business_id = request.args.get('id', None)

    if business_id is None:
        return jsonify({"error": "Must include a business ID"}) , 400

    try:
        oid = ObjectId(business_id)
    except:
        return jsonify({"error": "Not a valid business ID"}) , 400

    business = await db.businesses.delete_one({"_id": oid})

    if business.deleted_count == 0:
        return jsonify({"error": "Business not found"}) , 404

    return jsonify({"deleted": business_id}), 200

if __name__ == "__main__":
    app.run(debug=True)