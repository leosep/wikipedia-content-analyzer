from decouple import config
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings:
    WIKIPEDIA_USER_AGENT: str = "wikipedia-content-analyzer/1.0 (leandro.sepulveda@gmail.com)"
    PROJECT_NAME: str = "Wikipedia Content Analyzer"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = config("DATABASE_URL", cast=str)
    WIKIPEDIA_API_BASE_URL: str = config("WIKIPEDIA_API_BASE_URL", cast=str)

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()