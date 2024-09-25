import re

from typing import Tuple

import uuid
import pymupdf
from utils import get_vector_db



def extract_text_from_pdf(file_path: str) -> Tuple[str, str]:
    with pymupdf.open(file_path) as pdf_file:
        pdf_text = ""
        for page in pdf_file:
            pdf_text += page.get_text()
    
    pdf_text = re.sub('\n', ' ', pdf_text)      
    file_name = file_path.split('.pdf')[0]                
    return pdf_text, file_name


def convert_to_embeddings(pdf_text: str) -> None:
    vector_db = get_vector_db()
    file_text, file_name = extract_text_from_pdf(pdf_text)
    doc_id = str(uuid.uuid4())
    vector_db.add_texts(
        texts=[file_text],
        metadatas=[{"source": file_name, "id": doc_id}],
        ids=[doc_id]
    )
    return doc_id

