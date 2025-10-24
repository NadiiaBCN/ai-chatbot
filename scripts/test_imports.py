#!/usr/bin/env python3
"""Test all imports."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing imports...")

try:
    print("✓ Importing core...")
    from src.core import settings, setup_logging

    print("✓ Importing services...")
    from src.services.llm import OpenAIService
    from src.services.knowledge import DocumentLoader, Chunker, Retriever
    from src.services.memory import ConversationMemory

    print("✓ Importing vectorstore...")
    from src.vectorstore import PineconeStore, DocumentIndexer

    print("✓ Importing bot...")
    from src.bot import BotDispatcher

    print("✓ Importing API...")
    from src.api import app

    print("\n✅ All imports successful!")

except Exception as e:
    print(f"\n❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
