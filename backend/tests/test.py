import os
import sys
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.server.app import app

client = TestClient(app)

sys.path.append(os.getcwd())

def test_businesses():
    res = client.get("/business/")
    body = res.json()
    assert res.status_code == 200
    assert "data" in body