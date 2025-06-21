import pytest
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import Base, get_db
from app.database.models import Article
import app.database.models
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.crud.article import CRUDArticle
from typing import List, Tuple

TEST_DATABASE_URL = "sqlite:///./test_crud.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

article_crud = CRUDArticle()
TEST_USER_ID = 1 

@pytest.fixture(name="db_session_crud")
def db_session_crud_fixture():
    """
    Provides a SQLAlchemy session for testing CRUD operations.
    Ensures a clean database state for each test by creating and dropping tables.
    """

    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

def test_create_article(db_session_crud):
    """
    Test case for creating a new article.
    Verifies that the article is created with correct data and an ID is assigned.
    """
    article_data = ArticleCreate(
        wikipedia_title="Artículo de prueba",
        wikipedia_url="http://test.com/test_article",
        processed_summary="Este es un resumen de prueba.",
        word_count=5,
        frequent_words=[("test", 3), ("resumen", 2), ("prueba", 1)],
        personal_notes="Notas de prueba para creación.",
        user_id=TEST_USER_ID
    )
    article = article_crud.create_article(db_session_crud, article_data)

    assert article.id is not None
    assert article.wikipedia_title == "Artículo de prueba"
    assert article.wikipedia_url == "http://test.com/test_article"
    assert article.processed_summary == "Este es un resumen de prueba."
    assert article.word_count == 5
    assert article.frequent_words == [["test", 3], ["resumen", 2], ["prueba", 1]]
    assert article.personal_notes == "Notas de prueba para creación."
    assert article.user_id == TEST_USER_ID

def test_get_article(db_session_crud):
    """
    Test case for retrieving a single article by its ID.
    Checks for both existing and non-existing articles.
    """
    article_data = ArticleCreate(
        wikipedia_title="Otro artículo de prueba",
        wikipedia_url="http://test.com/another_test_article",
        processed_summary="Este es un resumen de prueba.",
        word_count=7,
        frequent_words=[("otro", 5), ("articulo", 3), ("prueba", 2)],
        personal_notes="Notas para otro artículo.",
        user_id=TEST_USER_ID
    )

    created_article = article_crud.create_article(db_session_crud, article_data)
    retrieved_article = article_crud.get_article(db_session_crud, created_article.id)

    assert retrieved_article is not None
    assert retrieved_article.id == created_article.id
    assert retrieved_article.wikipedia_title == "Otro artículo de prueba"
    assert retrieved_article.frequent_words == [["otro", 5], ["articulo", 3], ["prueba", 2]]

    non_existent_article = article_crud.get_article(db_session_crud, 999)
    assert non_existent_article is None

def test_get_articles(db_session_crud):
    """
    Test case for retrieving multiple articles with skip and limit parameters.
    """

    article_crud.create_article(db_session_crud, ArticleCreate(
        wikipedia_title="Artículo 1", wikipedia_url="http://a1.com", processed_summary="s1", word_count=1,
        frequent_words=[("word1", 10)], 
        personal_notes="", user_id=TEST_USER_ID
    ))
    article_crud.create_article(db_session_crud, ArticleCreate(
        wikipedia_title="Artículo 2", wikipedia_url="http://a2.com", processed_summary="s2", word_count=1,
        frequent_words=[("word2", 20)], 
        personal_notes="", user_id=TEST_USER_ID
    ))
    article_crud.create_article(db_session_crud, ArticleCreate(
        wikipedia_title="Artículo 3", wikipedia_url="http://a3.com", processed_summary="s3", word_count=1,
        frequent_words=[("word3", 30)], 
        personal_notes="", user_id=TEST_USER_ID
    ))

    articles = article_crud.get_articles(db_session_crud, skip=0, limit=2)
    assert len(articles) == 2
    assert articles[0].wikipedia_title == "Artículo 1"
    assert articles[1].wikipedia_title == "Artículo 2"

    articles_skipped = article_crud.get_articles(db_session_crud, skip=1, limit=2)
    assert len(articles_skipped) == 2
    assert articles_skipped[0].wikipedia_title == "Artículo 2"
    assert articles_skipped[1].wikipedia_title == "Artículo 3"

def test_update_article(db_session_crud):
    """
    Test case for updating an existing article.
    Checks if specific fields can be updated and if non-existent articles are handled.
    """
    initial_frequent_words = [("actualizar", 1)]
    article_data = ArticleCreate(
        wikipedia_title="Artículo actualizable",
        wikipedia_url="http://test.com/updatable_article",
        processed_summary="Resumen a actualizar.",
        word_count=3,
        frequent_words=initial_frequent_words,
        personal_notes="Notas iniciales.",
        user_id=TEST_USER_ID
    )
    created_article = article_crud.create_article(db_session_crud, article_data)

    update_data = ArticleUpdate(
        personal_notes="Notas personales actualizadas.",
        frequent_words=[("nueva_palabra", 99), ("palabra_prueba", 12)] 
    )
    updated_article = article_crud.update_article(db_session_crud, created_article.id, update_data)

    assert updated_article is not None
    assert updated_article.personal_notes == "Notas personales actualizadas."
    assert updated_article.wikipedia_title == "Artículo actualizable"

    assert updated_article.frequent_words == [["actualizar", 1]] 

    non_existent_update = article_crud.update_article(db_session_crud, 999, update_data)
    assert non_existent_update is None

def test_delete_article(db_session_crud):
    """
    Test case for deleting an article.
    Verifies that the article is deleted and no longer retrievable.
    """
    article_data = ArticleCreate(
        wikipedia_title="Artículo eliminable",
        wikipedia_url="http://test.com/deletable_article",
        processed_summary="Resumen a eliminar.",
        word_count=4,
        frequent_words=[("eliminar", 1), ("old_word", 2)],
        personal_notes="Artículo a ser eliminado.",
        user_id=TEST_USER_ID
    )
    created_article = article_crud.create_article(db_session_crud, article_data)

    deleted_article = article_crud.delete_article(db_session_crud, created_article.id)
    assert deleted_article is not None
    assert deleted_article.id == created_article.id

    retrieved_after_delete = article_crud.get_article(db_session_crud, created_article.id)
    assert retrieved_after_delete is None

    non_existent_delete = article_crud.delete_article(db_session_crud, 999)
    assert non_existent_delete is None