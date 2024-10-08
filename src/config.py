from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_id: str
    bq_dataset_id: str
    bq_table_name: str
    location: str
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
