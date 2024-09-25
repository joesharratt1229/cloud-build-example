import os
import tempfile

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from services.upload import convert_to_embeddings


router = APIRouter(prefix='/file', tags=['file'])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    if not req.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
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
                        "doc_id": doc_id
                    }
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred")
    finally:
        os.unlink(temp_file_path)