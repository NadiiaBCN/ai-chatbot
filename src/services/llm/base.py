"""Base LLM service."""

from abc import ABC, abstractmethod
from typing import List


class BaseLLMService(ABC):
    """Abstract LLM service."""

    @abstractmethod
    async def generate_answer(self, context: str, question: str) -> str:
        """Generate answer from context and question."""
        pass

    @abstractmethod
    async def create_embedding(self, text: str) -> List[float]:
        """Create text embedding."""
        pass
