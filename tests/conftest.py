import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.utils import get_vector_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def vector_db():
    return get_vector_db()
