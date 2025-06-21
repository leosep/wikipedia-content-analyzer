from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional
from typing import Optional, List, Tuple

class ArticleCreate(BaseModel):
    wikipedia_title: str
    wikipedia_url: HttpUrl
    processed_summary: str
    word_count: int
    frequent_words: List[Tuple[str, int]] = Field(default_factory=list)
    personal_notes: Optional[str] = None
    sentiment_polarity: Optional[float] = None
    sentiment_subjectivity: Optional[float] = None
    sentiment_label: Optional[str] = None
    user_id: int
    
class ArticleUpdate(BaseModel):
    personal_notes: Optional[str] = None

class ArticleInDB(ArticleCreate):
    id: int
    created_at: datetime | None = None
    saved_at: datetime | None = None

    class Config:
        from_attributes = True