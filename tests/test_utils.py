from unittest.mock import MagicMock, patch

from src.config import Settings
from src.utils import get_vector_db


# decorators applied bottom to top, but their mocks are injected left to right
@patch("src.utils.get_settings")
@patch("src.utils.VertexAIEmbeddings")
@patch("src.utils.BigQueryVectorSearch")
def test_get_vector_db(
    mock_bq_vector_search, mock_vertex_ai_embeddings, mock_get_settings
):
    mock_settings = MagicMock(spec=Settings)
    mock_settings.project_id = "test-project"
    mock_settings.bq_dataset_id = "test-dataset"
    mock_settings.bq_table_name = "test-table"
    mock_settings.location = "test-location"

    mock_embedding_model = MagicMock()
    mock_vector_db = MagicMock()

    # Setup mock objects
    mock_get_settings.return_value = mock_settings
    mock_vertex_ai_embeddings.return_value = mock_embedding_model

    mock_bq_vector_search.return_value = mock_vector_db

    # Call the function
    result = get_vector_db()

    # Assertions
    mock_vertex_ai_embeddings.assert_called_once_with(
        model_name="textembedding-gecko@latest", project=mock_settings.project_id
    )

    mock_bq_vector_search.assert_called_once_with(
        project_id=mock_settings.project_id,
        dataset_name=mock_settings.bq_dataset_id,
        table_name=mock_settings.bq_table_name,
        location=mock_settings.location,
        embedding=mock_embedding_model,
        distance_strategy="COSINE",
    )

    assert result == mock_vector_db
