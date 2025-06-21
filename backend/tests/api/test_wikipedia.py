import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings
from app.database.session import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture(name="db_session")
def db_session_fixture():
    """Create a test database session with a fresh table for each test."""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    app.dependency_overrides[get_db] = lambda: session

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)


def test_search_wikipedia():
    """Test the Wikipedia search endpoint."""
    response = client.get(f"{settings.API_V1_STR}/wikipedia/search?query=Python")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "url" in data[0]
        assert "pageid" in data[0]

    response = client.get(f"{settings.API_V1_STR}/wikipedia/search?query=")
    assert response.status_code == 422

def test_get_article_with_analysis():
    """Test the Wikipedia article detail and analysis endpoint."""
    response = client.get(f"{settings.API_V1_STR}/wikipedia/article/FastAPI")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "FastAPI"
    assert "summary" in data
    assert data["word_count"] > 0
    assert isinstance(data["frequent_words"], list)
    assert len(data["frequent_words"]) <= 10

    assert "sentiment_polarity" in data
    assert isinstance(data["sentiment_polarity"], float)
    assert -1.0 <= data["sentiment_polarity"] <= 1.0
    assert "sentiment_subjectivity" in data
    assert isinstance(data["sentiment_subjectivity"], float)
    assert 0.0 <= data["sentiment_subjectivity"] <= 1.0
    assert "sentiment_label" in data
    assert isinstance(data["sentiment_label"], str)
    assert data["sentiment_label"] in ["positive", "negative", "neutral"]

    response = client.get(f"{settings.API_V1_STR}/wikipedia/article/NoExiste")
    assert response.status_code == 200