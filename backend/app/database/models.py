from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from app.database.session import Base

import os
if os.getenv("DATABASE_URL") and "postgresql" in os.getenv("DATABASE_URL"):
    JSON_COLUMN_TYPE = JSONB
else: 
    JSON_COLUMN_TYPE = SQLiteJSON

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    wikipedia_title = Column(String, index=True, nullable=False)
    wikipedia_url = Column(String, nullable=False)
    processed_summary = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    frequent_words = Column(JSON_COLUMN_TYPE, nullable=False) 
    sentiment_polarity = Column(Float, nullable=True)
    sentiment_subjectivity = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=True)
    personal_notes = Column(String, nullable=True)
    saved_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=True)

    def __repr__(self):
        return f"<Article(title='{self.wikipedia_title}')>"