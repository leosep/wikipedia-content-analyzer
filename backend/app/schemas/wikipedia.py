from typing import List, Optional, Tuple
from pydantic import BaseModel, HttpUrl

class WikipediaSearchArticle(BaseModel):
    title: str
    pageid: Optional[int] = None
    url: Optional[HttpUrl] = None

class WikipediaArticleDetail(BaseModel):
    title: str
    summary: str
    full_url: str
    content: str
    references: List[str]
    url: str
    word_count: int
    frequent_words: List[Tuple[str, int]]
    sentiment_polarity: float 
    sentiment_subjectivity: float 
    sentiment_label: str
   