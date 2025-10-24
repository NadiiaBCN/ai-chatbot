"""Test configuration."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "This is a test document. It has multiple sentences. This is for testing."


@pytest.fixture
def temp_doc_file(tmp_path):
    """Create temporary document file."""
    file = tmp_path / "test.txt"
    file.write_text("Test document content")
    return file
