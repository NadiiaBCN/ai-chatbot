"""Document indexing service."""

import asyncio
from pathlib import Path
from typing import Set, Dict, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from loguru import logger

from src.core import settings
from src.services.knowledge import DocumentLoader, Chunker
from src.vectorstore.pinecone_store import PineconeStore


class DocumentEventHandler(FileSystemEventHandler):
    """File system event handler."""

    def __init__(self, indexer: 'DocumentIndexer', loop: asyncio.AbstractEventLoop):
        self.indexer = indexer
        self.loop = loop

    def _is_supported(self, filepath: str) -> bool:
        """Check if file is supported."""
        return any(filepath.endswith(ext) for ext in settings.supported_extensions)

    def _schedule_task(self, coro):
        """Schedule coroutine in the main event loop."""
        try:
            asyncio.run_coroutine_threadsafe(coro, self.loop)
        except Exception as e:
            logger.error(f"Failed to schedule task: {e}")

    def on_created(self, event: FileSystemEvent):
        """Handle file creation."""
        if not event.is_directory and self._is_supported(event.src_path):
            logger.info(f"New file: {event.src_path}")
            self._schedule_task(self.indexer.index_file(Path(event.src_path)))

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification."""
        if not event.is_directory and self._is_supported(event.src_path):
            logger.info(f"Modified: {event.src_path}")
            self._schedule_task(
                self.indexer.reindex_file(Path(event.src_path)))

    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion."""
        if not event.is_directory and self._is_supported(event.src_path):
            logger.info(f"Deleted: {event.src_path}")
            self._schedule_task(self.indexer.remove_file(Path(event.src_path)))


class DocumentIndexer:
    """Index documents to vector store."""

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = Chunker()
        self.vectorstore = PineconeStore()
        self.indexed_files: Set[str] = set()
        self.file_hashes: Dict[str, str] = {}
        self.observer = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def index_file(self, filepath: Path) -> bool:
        """Index a single file."""
        try:
            # Load document
            content = self.loader.load_document(filepath)
            if not content:
                return False

            # Calculate hash
            doc_hash = self.loader.calculate_hash(content)

            # Check if already indexed
            if doc_hash in self.file_hashes.values():
                logger.info(f"Already indexed: {filepath.name}")
                return True

            # Create chunks
            chunks = self.chunker.create_chunks(content)

            # Upsert to vector store
            metadata = {
                "filename": filepath.name,
                "file_type": filepath.suffix
            }
            await self.vectorstore.upsert(doc_hash, chunks, metadata)

            # Track indexed file
            self.indexed_files.add(str(filepath))
            self.file_hashes[str(filepath)] = doc_hash

            logger.info(f"Indexed: {filepath.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to index {filepath}: {e}")
            return False

    async def reindex_file(self, filepath: Path) -> bool:
        """Reindex modified file."""
        try:
            # Get old hash
            old_hash = self.file_hashes.get(str(filepath))

            # Load new content
            content = self.loader.load_document(filepath)
            new_hash = self.loader.calculate_hash(content)

            # Check if changed
            if old_hash == new_hash:
                return True

            # Delete old vectors
            if old_hash:
                self.vectorstore.delete(old_hash)

            # Index new version
            return await self.index_file(filepath)

        except Exception as e:
            logger.error(f"Failed to reindex {filepath}: {e}")
            return False

    async def remove_file(self, filepath: Path) -> bool:
        """Remove file vectors."""
        try:
            doc_hash = self.file_hashes.get(str(filepath))
            if doc_hash:
                self.vectorstore.delete(doc_hash)
                self.indexed_files.discard(str(filepath))
                del self.file_hashes[str(filepath)]
                logger.info(f"Removed: {filepath.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove {filepath}: {e}")
            return False

    async def index_all(self) -> Dict:
        """Index all documents in folder."""
        try:
            folder = Path(settings.documents_folder)
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
                logger.warning(f"Created documents folder: {folder}")

            files = []
            for ext in settings.supported_extensions:
                files.extend(folder.glob(f"**/*{ext}"))

            results = {"total": len(files), "success": 0, "failed": 0}

            for filepath in files:
                success = await self.index_file(filepath)
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1

            logger.info(
                f"Indexed {results['success']}/{results['total']} documents")
            return results

        except Exception as e:
            logger.error(f"Failed to index all: {e}")
            return {"error": str(e)}

    def start_watching(self):
        """Start watching documents folder."""
        try:
            # Get the current event loop
            self.loop = asyncio.get_event_loop()

            folder = Path(settings.documents_folder)
            folder.mkdir(parents=True, exist_ok=True)

            event_handler = DocumentEventHandler(self, self.loop)
            self.observer = Observer()
            self.observer.schedule(event_handler, str(folder), recursive=True)
            self.observer.start()

            logger.info(f"Watching: {folder}")

        except Exception as e:
            logger.error(f"Failed to start watching: {e}")
            raise

    def stop_watching(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped watching")
