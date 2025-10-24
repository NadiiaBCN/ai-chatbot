"""Chat routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from src.services.knowledge import Retriever

router = APIRouter()
retriever = Retriever()


class QueryRequest(BaseModel):
    """Query request."""
    query: str
    top_k: int = 5
    threshold: float = 0.7


class QueryResponse(BaseModel):
    """Query response."""
    answer: str
    sources: List[str]
    confidence: float


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query knowledge base."""
    try:
        answer, sources, confidence = await retriever.retrieve_and_answer(
            question=request.query,
            top_k=request.top_k,
            threshold=request.threshold
        )
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
