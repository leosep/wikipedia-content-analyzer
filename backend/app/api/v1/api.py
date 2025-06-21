from app.api.v1.endpoints import wiki_api_routes
from fastapi import APIRouter
from app.api.v1.endpoints import articles

api_router = APIRouter()
api_router.include_router(wiki_api_routes.router, prefix="/wikipedia", tags=["wikipedia"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])