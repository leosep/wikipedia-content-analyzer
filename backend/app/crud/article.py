from sqlalchemy.orm import Session
from app.database.models import Article
from app.schemas.article import ArticleCreate, ArticleUpdate
from typing import List, Optional
from datetime import datetime
import json

class CRUDArticle:
    def create_article(self, db: Session, article: ArticleCreate) -> Article:
        db_article = Article(
            wikipedia_title=article.wikipedia_title,
            wikipedia_url=str(article.wikipedia_url),
            processed_summary=article.processed_summary,
            word_count=article.word_count,
            frequent_words=article.frequent_words,
            sentiment_polarity=article.sentiment_polarity,
            sentiment_subjectivity=article.sentiment_subjectivity,
            sentiment_label=article.sentiment_label,
            personal_notes=article.personal_notes,
            user_id=article.user_id,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        self._convert_frequent_words_for_schema(db_article)
        return db_article

    def get_articles(self, db: Session, skip: int = 0, limit: int = 10) -> List[Article]: # Ensure self is here and return type is List[Article]
        articles_from_db = db.query(Article).offset(skip).limit(limit).all()

        for article_obj in articles_from_db:
            if article_obj.frequent_words and isinstance(article_obj.frequent_words, str):
                try:
                    loaded_words = json.loads(article_obj.frequent_words)
                    
                    if isinstance(loaded_words, list) and all(isinstance(item, str) for item in loaded_words):
                        article_obj.frequent_words = [[word, 0] for word in loaded_words]
                    elif isinstance(loaded_words, list) and all(isinstance(item, list) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], (int, float)) for item in loaded_words):
                        article_obj.frequent_words = loaded_words
                    else:
                        article_obj.frequent_words = []
                except (json.JSONDecodeError, TypeError):
                    article_obj.frequent_words = [] 
            else:
                article_obj.frequent_words = []

        return articles_from_db

    def get_article(self, db: Session, article_id: int) -> Optional[Article]:
        return db.query(Article).filter(Article.id == article_id).first()

    def update_article(self, db: Session, article_id: int, article_update: ArticleUpdate) -> Optional[Article]:
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            update_data = article_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_article, key, value)
            db.add(db_article)
            db.commit()
            db.refresh(db_article)

            if isinstance(db_article.frequent_words, str):
                try:
                    loaded = json.loads(db_article.frequent_words)
                    if isinstance(loaded, list):
                        db_article.frequent_words = loaded
                    else:
                        db_article.frequent_words = []
                except json.JSONDecodeError:
                    db_article.frequent_words = []

        return db_article

    def delete_article(self, db: Session, article_id: int) -> Optional[Article]:
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            db.delete(db_article)
            db.commit()
        return db_article
    
    def _convert_frequent_words_for_schema(self, article_obj: Article) -> None:
        """Helper to convert frequent_words from DB format to schema expected format."""
        if article_obj.frequent_words and isinstance(article_obj.frequent_words, str):
            try:
                loaded_words = json.loads(article_obj.frequent_words)
                if isinstance(loaded_words, list) and all(isinstance(item, str) for item in loaded_words):
                    article_obj.frequent_words = [[word, 0] for word in loaded_words]
                elif isinstance(loaded_words, list) and all(isinstance(item, list) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], (int, float)) for item in loaded_words):
                    article_obj.frequent_words = loaded_words
                else:
                    article_obj.frequent_words = []
            except (json.JSONDecodeError, TypeError):
                article_obj.frequent_words = []
        elif article_obj.frequent_words is None:
            article_obj.frequent_words = [] 

article_crud = CRUDArticle()