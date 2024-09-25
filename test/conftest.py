import pytest
from fastapi.testclient import TestClient
from src.main import app  # Assuming your FastAPI app is in src/main.py

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
