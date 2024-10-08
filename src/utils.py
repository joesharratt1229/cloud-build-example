from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_google_community import BigQueryVectorSearch
from langchain_google_vertexai import VertexAIEmbeddings

from src.config import get_settings


@lru_cache
def get_vector_db() -> Embeddings:
    settings = get_settings()
    global vector_db
    embedding_model = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=settings.project_id
    )
    vector_db = BigQueryVectorSearch(
        project_id=settings.project_id,
        dataset_name=settings.bq_dataset_id,
        table_name=settings.bq_table_name,
        location=settings.location,
        embedding=embedding_model,
        distance_strategy="COSINE",
    )

    return vector_db
