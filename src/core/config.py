"""Configuration management."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Telegram
    telegram_bot_token: str

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-3-large"

    # Pinecone
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str

    # App
    app_name: str = "AI Chatbot"
    debug: bool = False
    log_level: str = "INFO"

    # Documents
    documents_folder: str = "./data/documents"
    max_chunk_size: int = 1000
    chunk_overlap: int = 200

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Vector DB
    vector_dimension: int = 2048
    top_k_results: int = 5
    similarity_threshold: float = 0.7

    # Rate Limiting
    max_requests_per_minute: int = 30

    @property
    def supported_extensions(self) -> List[str]:
        return [".txt", ".pdf", ".docx"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
