"""Health check routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.core import settings
from src.vectorstore import PineconeStore

router = APIRouter()
vectorstore = PineconeStore()


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database_connected: bool


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check application health."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database_connected=vectorstore.is_connected()
    )
