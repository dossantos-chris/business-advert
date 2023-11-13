from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/test", methods=["GET"])
def test():
    test = os.getenv("API_KEY")
    return jsonify({'test': f'{test}'})

if __name__ == "__main__":
    app.run(debug=True)