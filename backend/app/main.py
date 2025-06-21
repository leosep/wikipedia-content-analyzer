from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine
from app.database.models import Base

app = FastAPI(
    title="API del analizador de contenido de Wikipedia",
    description="API para buscar y analizar contenido de Wikipedia.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API del analizador de contenido de Wikipedia!"}