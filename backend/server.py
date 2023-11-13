from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.BusinessAdvert
CORS(app)

@app.route("/test", methods=["GET"])
async def test():
    business = db['businesses'].find_one({"name" : "Xina"}, {"_id": 0})  # Exclude _id field
    return jsonify({'business': business})

if __name__ == "__main__":
    app.run(debug=True)