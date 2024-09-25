import pytest
from fastapi.testclient import TestClient


def test_stream_chat(client):
    # Prepare test data
    chat_message = {"message": "What is the capital of France?"}

    # Send POST request to the /chat/stream endpoint
    response = client.post("/chat/stream", json=chat_message)

    # Check if the response is successful
    assert response.status_code == 200

    # Check if the response is a streaming response
    assert response.headers["content-type"] == "text/event-stream"

    # Read the streamed content
    content = b"".join(response.iter_content())

    # Check if the content is not empty
    assert len(content) > 0

    # You might want to add more specific checks based on the expected content
    # For example, check if "Paris" is in the response
    assert b"Paris" in content