"""
Semantic Pulse X - API principale
Cartographie dynamique des émotions médiatiques
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.backend.core.config import settings
from app.backend.api.routes import emotions, predictions, data_sources
from app.backend.api.wordcloud_routes import wordcloud_router
from app.backend.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Semantic Pulse X",
    description="Cartographie dynamique des émotions médiatiques",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(emotions, prefix="/api/v1/emotions", tags=["emotions"])
app.include_router(predictions, prefix="/api/v1/predictions", tags=["predictions"])
app.include_router(data_sources, prefix="/api/v1/sources", tags=["data-sources"])
app.include_router(wordcloud_router, prefix="/api/v1/wordcloud", tags=["wordcloud"])


@app.get("/")
async def root():
    return {
        "message": "Semantic Pulse X - Cartographie dynamique des émotions médiatiques",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "semantic-pulse-x"}
