#!/usr/bin/env python3
"""Manual document indexing."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import setup_logging
from src.vectorstore import DocumentIndexer


async def main():
    """Index all documents."""
    setup_logging()
    
    print("Starting document indexing...")
    
    indexer = DocumentIndexer()
    results = await indexer.index_all()
    
    print("\n" + "=" * 50)
    print("Indexing Results")
    print("=" * 50)
    print(f"Total: {results.get('total', 0)}")
    print(f"Success: {results.get('success', 0)}")
    print(f"Failed: {results.get('failed', 0)}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
