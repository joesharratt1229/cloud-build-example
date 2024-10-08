import os
import tempfile
from unittest.mock import patch

import pytest


@pytest.fixture
def sample_pdf_file():
    # Create a temporary PDF file for testing

    pdf_content = b"""%PDF-1.0
    1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
    2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
    3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj
    xref
    0 4
    0000000000 65535 f
    0000000010 00000 n
    0000000053 00000 n
    0000000102 00000 n
    trailer<</Size 4/Root 1 0 R>>
    startxref
    149
    %%EOF"""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf.write(pdf_content)
        temp_pdf_path = temp_pdf.name

    yield temp_pdf_path

    # Clean up the temporary file after the test
    os.unlink(temp_pdf_path)


@pytest.fixture
def sample_word_file():
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
        temp_docx.write(b"This is a sample Word file for testing.")
        temp_docx_path = temp_docx.name

    yield temp_docx_path

    os.unlink(temp_docx_path)


@pytest.fixture
def large_pdf_file():
    # Create a temporary large PDF file for testing
    large_pdf_content = b"%PDF-1.0" + b"\0" * (10 * 1024 * 1024 + 1)  # Just over 10 MB
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf.write(large_pdf_content)
        temp_pdf_path = temp_pdf.name

    yield temp_pdf_path

    # Clean up the temporary file after the test
    os.unlink(temp_pdf_path)


@patch("src.routers.upload.convert_to_embeddings")
def test_upload_file(mock_convert_to_embeddings, client, sample_pdf_file):
    mock_convert_to_embeddings.return_value = "mocked_doc_id"
    with open(sample_pdf_file, "rb") as file:
        response = client.post("/file/upload", files={"file": file})

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "File uploaded and processed successfully"
    assert "doc_id" in response_json
    assert "filename" in response_json


def test_upload_file_invalid_file(client, sample_word_file):
    with open(sample_word_file, "rb") as file:
        response = client.post("/file/upload", files={"file": file})
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"


def test_upload_file_too_large(client, large_pdf_file):
    with open(large_pdf_file, "rb") as file:
        response = client.post("/file/upload", files={"file": file})
    assert response.status_code == 400
    assert response.json()["detail"] == "File size is too large"
