from flask import Flask, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.BusinessAdvert
CORS(app)

@app.route("/", methods=["GET"])
async def home():
    return "<main>Home Page</main>"


@app.route("/test", methods=["GET"])
async def test():
    businessCursor = db.businesses.find({}, {"_id": 0})
    businesses = await businessCursor.to_list(None)
    return jsonify({"businesses": businesses})

if __name__ == "__main__":
    app.run(debug=True)