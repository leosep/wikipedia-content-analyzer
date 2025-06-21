import wikipedia
from typing import List, Optional
from collections import Counter
import re
from fastapi import HTTPException

from wikipedia.exceptions import DisambiguationError, PageError

from app.schemas.wikipedia import WikipediaSearchArticle, WikipediaArticleDetail
from app.core.config import settings

from textblob import TextBlob

class WikipediaService:
    def __init__(self):
        wikipedia.set_lang('es')

    def search_articles(self, query: str, limit: int = 10) -> List[WikipediaSearchArticle]:
        actual_limit = min(max(1, limit), 50)
        articles = []
        try:
            search_results_titles = wikipedia.search(query, results=actual_limit)

            for title in search_results_titles:
                try:
                    page = wikipedia.page(title, auto_suggest=False, redirect=True)
                    articles.append(WikipediaSearchArticle(
                        title=page.title,
                        pageid=str(page.pageid) if hasattr(page, 'pageid') else None,
                        url=page.url if hasattr(page, 'url') else None
                    ))
                except DisambiguationError:
                    articles.append(WikipediaSearchArticle(
                        title=title,
                        pageid=None,
                        url=None
                    ))
                except PageError:
                    articles.append(WikipediaSearchArticle(
                        title=title,
                        pageid=None,
                        url=None
                    ))
                except Exception:
                    articles.append(WikipediaSearchArticle(
                        title=title,
                        pageid=None,
                        url=None
                    ))
            return articles
        except Exception:
            return []

    def get_article_details(self, title: str) -> Optional[WikipediaArticleDetail]:
        page = None
        try:
            page = wikipedia.page(title, auto_suggest=True, redirect=True)
        except PageError:
            return None
        except DisambiguationError as e:
            raise HTTPException(
                status_code=400,
                detail=f"'{title}' es una página de desambiguación. Proporcione un título más específico. Opciones: {e.options[:5]}"
            )
        except Exception as e:
            return None

        if not page:
            return None

        try:
            content = page.content or ""
            words = re.findall(r'\b[a-zA-Záéíóúñ]{3,}\b', content.lower())

            stopwords = {
                'el', 'la', 'y', 'para', 'son', 'esto', 'eso', 'desde', 'con',
                'fue', 'fueron', 'tener', 'tiene', 'tenía', 'no', 'pero', 'tú',
                'tu', 'su', 'sus', 'acerca', 'cual', 'será', 'han sido', 'ellos', 'allí',
                'cuando', 'qué', 'quién', 'cómo', 'también', 'uno', 'dos', 'puede',
                'todos', 'más', 'algunos', 'cualquier', 'cada', 'la mayoría'
            }

            frequent_word_counts = Counter(w for w in words if w not in stopwords).most_common(10)
            frequent_words_for_schema = list(frequent_word_counts)

            references = list(page.references) if hasattr(page, 'references') else []
            page_url = page.url if hasattr(page, 'url') else ""

            blob = TextBlob(content)
            sentiment_polarity = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity

            sentiment_label = "neutral"
            if sentiment_polarity > 0.1:
                sentiment_label = "positivo"
            elif sentiment_polarity < -0.1:
                sentiment_label = "negativo"

            return WikipediaArticleDetail(
                title=page.title,
                summary=page.summary or "",
                full_url=page_url,
                content=content,
                references=references,
                url=page_url,
                word_count=len(words),
                frequent_words=frequent_words_for_schema,
                sentiment_polarity=sentiment_polarity,
                sentiment_subjectivity=sentiment_subjectivity,
                sentiment_label=sentiment_label
            )
        except Exception as e:
            return None
