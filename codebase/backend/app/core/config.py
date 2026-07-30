from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PI-RAG Security Checker"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./sqlite.db"

    # ChromaDB Vector Store
    CHROMA_PATH: str = "./chroma_db"
    CHROMA_HOST: str = ""
    CHROMA_PORT: int = 8000
    CHROMA_DEFAULT_COLLECTION: str = "default_collection"
    HF_EMBEDDING_MODEL: str = "bkai-foundation-models/vietnamese-bi-encoder"

    # LLM Settings (OpenRouter or Ollama)
    LLM_API_KEY: str = "ollama"
    LLM_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_MODEL: str = "openai/gpt-4o-mini"

    @property
    def CHROMA_PERSIST_DIRECTORY(self) -> str:
        return self.CHROMA_PATH

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

