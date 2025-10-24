"""Unit tests for chunker."""

import pytest
from src.services.knowledge import Chunker


class TestChunker:
    """Test text chunking."""
    
    @pytest.fixture
    def chunker(self):
        """Create chunker instance."""
        return Chunker()
    
    def test_split_sentences(self, chunker, sample_text):
        """Test sentence splitting."""
        sentences = chunker.split_sentences(sample_text)
        assert len(sentences) > 0
        assert all(isinstance(s, str) for s in sentences)
    
    def test_create_chunks(self, chunker, sample_text):
        """Test chunk creation."""
        chunks = chunker.create_chunks(sample_text)
        assert len(chunks) > 0
        assert all(isinstance(c, str) for c in chunks)
