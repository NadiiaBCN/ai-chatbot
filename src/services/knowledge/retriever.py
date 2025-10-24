"""Knowledge retrieval service."""

from typing import List, Dict, Tuple
from loguru import logger

from src.services.llm import OpenAIService
from src.vectorstore import PineconeStore


class Retriever:
    """Retrieve relevant knowledge."""
    
    def __init__(self):
        self.llm = OpenAIService()
        self.vectorstore = PineconeStore()
    
    async def retrieve_and_answer(
        self, 
        question: str, 
        top_k: int = 5, 
        threshold: float = 0.7
    ) -> Tuple[str, List[str], float]:
        """Retrieve context and generate answer."""
        try:
            # Search similar documents
            results = await self.vectorstore.search(question, top_k, threshold)
            
            if not results:
                # Fallback to general knowledge
                answer = await self.llm.generate_answer("", question)
                return answer, [], 0.0
            
            # Build context
            context_parts = []
            sources = []
            scores = []
            
            for result in results:
                context_parts.append(f"[{result['filename']}]\n{result['content']}")
                if result['filename'] not in sources:
                    sources.append(result['filename'])
                scores.append(result['score'])
            
            context = "\n\n".join(context_parts)
            avg_score = sum(scores) / len(scores)
            
            # Generate answer
            answer = await self.llm.generate_answer(context, question)
            
            logger.info(f"Answer generated with {len(sources)} sources")
            return answer, sources, avg_score
            
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            raise
