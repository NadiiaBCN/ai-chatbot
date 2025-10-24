"""OpenAI LLM service."""

from openai import AsyncOpenAI
from typing import List
from loguru import logger

from src.core import settings
from src.core.exceptions import LLMError
from src.services.llm.base import BaseLLMService


class OpenAIService(BaseLLMService):
    """OpenAI integration."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_answer(self, context: str, question: str) -> str:
        """Generate answer using GPT-4."""
        try:
            prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""

            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise LLMError(f"Failed to generate answer: {e}")

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding using OpenAI text-embedding-3-large (default 3072 dimensions)."""
        try:
            response = await self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text
            )

            embedding = response.data[0].embedding

            # Truncate or pad to match Pinecone dimension
            target_dim = settings.vector_dimension
            current_dim = len(embedding)

            if current_dim > target_dim:
                # Truncate if embedding is larger
                embedding = embedding[:target_dim]
                logger.debug(
                    f"Truncated embedding from {current_dim} to {target_dim}")
            elif current_dim < target_dim:
                # Pad with zeros if embedding is smaller
                embedding = embedding + [0.0] * (target_dim - current_dim)
                logger.debug(
                    f"Padded embedding from {current_dim} to {target_dim}")

            return embedding

        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            raise LLMError(f"Failed to create embedding: {e}")
