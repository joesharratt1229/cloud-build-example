import pytest
from fastapi.testclient import TestClient
from src.main import app  # Assuming your FastAPI app is in src/main.py



def test_upload_file(client):
    test_file_content = b"This is a test file content"
    files = {"file": ("test_file.txt", test_file_content, "text/plain")}

    response = client.post("/upload", files=files)

    assert response.status_code == 200

    response_json = response.json()
    assert "filename" in response_json
    assert response_json["filename"] == "test_file.txt"