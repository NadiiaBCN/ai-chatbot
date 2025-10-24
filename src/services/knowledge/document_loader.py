"""Document loading service."""

import hashlib
from pathlib import Path
from typing import Optional
import PyPDF2
import docx
from loguru import logger

from src.core.exceptions import DocumentProcessingError


class DocumentLoader:
    """Load and extract text from documents."""
    
    def calculate_hash(self, content: str) -> str:
        """Calculate SHA256 hash."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def load_txt(self, filepath: Path) -> str:
        """Load TXT file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_pdf(self, filepath: Path) -> str:
        """Load PDF file."""
        text = []
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    def load_docx(self, filepath: Path) -> str:
        """Load DOCX file."""
        doc = docx.Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])
    
    def load_document(self, filepath: Path) -> Optional[str]:
        """Load document based on extension."""
        try:
            ext = filepath.suffix.lower()
            
            if ext == '.txt':
                return self.load_txt(filepath)
            elif ext == '.pdf':
                return self.load_pdf(filepath)
            elif ext == '.docx':
                return self.load_docx(filepath)
            else:
                logger.warning(f"Unsupported file type: {ext}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            raise DocumentProcessingError(f"Failed to load document: {e}")
