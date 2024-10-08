import os
import tempfile

from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.services.upload import convert_to_embeddings

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size is too large")

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        doc_id = convert_to_embeddings(temp_file_path)

        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded and processed successfully",
                "filename": file.filename,
                "doc_id": doc_id,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
