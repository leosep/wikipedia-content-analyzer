import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.crud.article import article_crud
from app.schemas.article import ArticleCreate, ArticleInDB, ArticleUpdate
from app.database.session import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=ArticleInDB, status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    """
    Saves a Wikipedia article to the database.
    """
    db_article = article_crud.create_article(db, article)
    return db_article

@router.get("/{article_id}", response_model=ArticleInDB)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a saved article by its ID.
    """
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado.")
    return db_article

@router.get("/", response_model=List[ArticleInDB])
async def get_saved_articles(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Retrieves a list of saved articles with pagination.
    """
    articles = article_crud.get_articles(db, skip=skip, limit=limit)
    return articles

@router.patch("/{article_id}", response_model=ArticleInDB)
async def update_article_notes(article_id: int, article_update: ArticleUpdate, db: Session = Depends(get_db)):
    """
    Updates personal notes for a saved article.
    """
    db_article = article_crud.update_article(db, article_id, article_update)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado.")
    return db_article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Deletes a saved article from the database.
    """
    db_article = article_crud.delete_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado.")
    return