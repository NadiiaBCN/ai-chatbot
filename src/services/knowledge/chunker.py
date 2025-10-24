"""Text chunking service."""

import re
from typing import List
from loguru import logger

from src.core import settings


class Chunker:
    """Split text into chunks."""
    
    def __init__(self):
        self.max_size = settings.max_chunk_size
        self.overlap = settings.chunk_overlap
    
    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        pattern = re.compile(r'[.!?]+[\s\n]+')
        sentences = pattern.split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def create_chunks(self, text: str) -> List[str]:
        """Create overlapping chunks."""
        sentences = self.split_sentences(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.max_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                
                # Create overlap
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= self.overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        logger.debug(f"Created {len(chunks)} chunks")
        return chunks
