"""Pinecone vector store."""

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
from loguru import logger

from src.core import settings
from src.core.exceptions import VectorDBError
from src.services.llm import OpenAIService


class PineconeStore:
    """Pinecone vector database."""

    def __init__(self):
        self.llm = OpenAIService()
        self._init_pinecone()

    def _init_pinecone(self):
        """Initialize Pinecone."""
        try:
            self.pc = Pinecone(api_key=settings.pinecone_api_key)

            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]

            if settings.pinecone_index_name not in existing_indexes:
                self.pc.create_index(
                    name=settings.pinecone_index_name,
                    dimension=settings.vector_dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.pinecone_environment
                    )
                )
                logger.info(
                    f"Created Pinecone index: {settings.pinecone_index_name}")

            self.index = self.pc.Index(settings.pinecone_index_name)
            logger.info("Pinecone initialized")

        except Exception as e:
            logger.error(f"Pinecone init error: {e}")
            raise VectorDBError(f"Failed to initialize Pinecone: {e}")

    async def upsert(self, doc_id: str, chunks: List[str], metadata: Dict):
        """Upsert document chunks."""
        try:
            vectors = []

            for idx, chunk in enumerate(chunks):
                embedding = await self.llm.create_embedding(chunk)

                vector = {
                    "id": f"{doc_id}_chunk_{idx}",
                    "values": embedding,
                    "metadata": {
                        "document_id": doc_id,
                        "content": chunk,
                        "chunk_index": idx,
                        **metadata
                    }
                }
                vectors.append(vector)

            # Batch upsert
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)

            logger.info(f"Upserted {len(vectors)} vectors")

        except Exception as e:
            logger.error(f"Upsert error: {e}")
            raise VectorDBError(f"Failed to upsert: {e}")

    async def search(self, query: str, top_k: int, threshold: float) -> List[Dict]:
        """Search similar vectors."""
        try:
            embedding = await self.llm.create_embedding(query)

            results = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )

            matches = []
            for match in results.matches:
                if match.score >= threshold:
                    matches.append({
                        "id": match.id,
                        "score": match.score,
                        "content": match.metadata.get("content", ""),
                        "filename": match.metadata.get("filename", ""),
                        "document_id": match.metadata.get("document_id", "")
                    })

            logger.info(f"Found {len(matches)} matches")
            return matches

        except Exception as e:
            logger.error(f"Search error: {e}")
            raise VectorDBError(f"Search failed: {e}")

    def delete(self, doc_id: str):
        """Delete document vectors."""
        try:
            # Delete by metadata filter
            self.index.delete(filter={"document_id": {"$eq": doc_id}})
            logger.info(f"Deleted vectors for {doc_id}")
        except Exception as e:
            logger.error(f"Delete error: {e}")
            raise VectorDBError(f"Delete failed: {e}")

    def is_connected(self) -> bool:
        """Check connection."""
        try:
            self.index.describe_index_stats()
            return True
        except:
            return False
