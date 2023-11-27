#pytest tests/business_tests.py -W ignore::DeprecationWarning -s
import pytest
import json

test_business = {"name": "Test",
                "service": "Test",
                "city": "Test",
                "state": "Test"}

@pytest.mark.anyio
async def test_get_businesses(test_client):
    res = await test_client.get("/business/")
    body = res.json()
    print(body)
    assert res.status_code == 200

@pytest.mark.anyio
async def test_get_business_data(test_client):
    res = await test_client.get("/business/65544103be35ac9661db908f")
    body = res.json()
    print(body)
    assert res.status_code == 200

@pytest.mark.anyio
async def test_add_and_delete_business_data(test_client):
    res = await test_client.post("/business/", data=json.dumps(test_business))
    body = res.json()
    print(body)
    id = body["data"]["_id"]
    res = await test_client.delete(f"/business/{id}")
    body = res.json()
    print(body)
    assert res.status_code == 200

@pytest.mark.anyio
async def test_update_business_data(test_client):
    res = await test_client.put("/business/65544103be35ac9661db908f", data=json.dumps(test_business))
    body = res.json()
    print(body)
    assert res.status_code == 200