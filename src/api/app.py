"""FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core import settings
from src.api.routes import health, chat

app = FastAPI(title=settings.app_name, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "running"
    }
