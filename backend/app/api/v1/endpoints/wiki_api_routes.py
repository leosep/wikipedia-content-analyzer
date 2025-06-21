from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas.wikipedia import WikipediaSearchArticle, WikipediaArticleDetail
from app.services.wikipedia_api import WikipediaService

router = APIRouter()

def get_wikipedia_service():
    return WikipediaService()

@router.get(
    "/search", 
    response_model=List[WikipediaSearchArticle],
    summary="Buscar artículos de Wikipedia",
    description="Busca en Wikipedia y devuelve una lista de artículos coincidentes."
)
async def search_wikipedia_articles(
    query: str = Query(..., min_length=1, max_length=100, description="Consulta de búsqueda de Wikipedia"),

    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados de búsqueda a devolver (1-50)")
) -> List[WikipediaSearchArticle]:
    """
    Handles the search for Wikipedia articles.
    """
    service = get_wikipedia_service()
    articles = service.search_articles(query, limit=limit)
    return articles

@router.get(
    "/article/{title}",
    response_model=Optional[WikipediaArticleDetail],
    summary="Detalles del artículo de Wikipedia",
    description="Obtiene el contenido detallado de un artículo específico de Wikipedia por título."
)
async def get_wikipedia_article_details(
    title: str
) -> Optional[WikipediaArticleDetail]:
    """
    Handles fetching detailed Wikipedia article content.
    """
    service = get_wikipedia_service()
    article = service.get_article_details(title)
    if not article:
        raise HTTPException(status_code=404, detail=f"Artículo '{title}' no encontrado.")
    return article