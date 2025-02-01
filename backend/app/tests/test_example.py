import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_example_endpoint():
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}  # 根据实际返回值调整

def test_example_post():
    response = client.post("/api/v1/example", json={"data": "test"})
    assert response.status_code == 201
    assert response.json() == {"data": "test", "status": "success"}  # 根据实际返回值调整