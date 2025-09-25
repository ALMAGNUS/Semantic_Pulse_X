"""
Configuration centralisée - Semantic Pulse X
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Database
    database_url: str = "sqlite:///./semantic_pulse.db"
    
    # MinIO/S3
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "admin"
    minio_secret_key: str = "admin123"
    minio_bucket: str = "semantic-pulse"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # API Keys
    twitter_bearer_token: Optional[str] = None
    newsapi_key: Optional[str] = None
    youtube_api_key: Optional[str] = None
    instagram_access_token: Optional[str] = None
    
    # Ollama
    ollama_host: str = "localhost:11434"
    
    # Monitoring
    prometheus_port: int = 9090
    grafana_port: int = 3000
    
    # AI Models
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"
    
    # Data Processing
    batch_size: int = 1000
    max_text_length: int = 512
    
    class Config:
        env_file = ".env"


settings = Settings()
