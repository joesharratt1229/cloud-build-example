from unittest.mock import patch

from src.config import get_settings


@patch("src.config.Settings")
def test_get_settings(MockSettings):
    mock_settings = MockSettings.return_value
    mock_settings.project_id = "test-project"
    mock_settings.bq_dataset_id = "test-dataset"
    mock_settings.bq_table_name = "test-table"
    mock_settings.location = "test-location"
    mock_settings.openai_api_key = "test-key"

    result = get_settings()
    assert result == mock_settings
