import re
import uuid
from typing import Tuple

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils import get_vector_db


def extract_text_from_pdf(file_path: str) -> Tuple[str, str]:
    with pymupdf.open(file_path) as pdf_file:
        pdf_text = ""
        for page in pdf_file:
            pdf_text += page.get_text()

    pdf_text = re.sub("\n", " ", pdf_text)
    file_name = file_path.split(".pdf")[0]
    return pdf_text, file_name


def convert_to_embeddings(
    pdf_text: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> str:
    vector_db = get_vector_db()
    file_text, file_name = extract_text_from_pdf(pdf_text)
    doc_id = str(uuid.uuid4())

    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(file_text)

    # Add chunks to the vector database
    vector_db.add_texts(
        texts=chunks,
        metadatas=[{"source": file_name, "id": doc_id} for _ in chunks],
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
    )

    return doc_id
