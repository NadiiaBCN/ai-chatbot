"""Main application entry point."""

import asyncio
import uvicorn
from contextlib import asynccontextmanager
from loguru import logger

from src.core import settings, setup_logging
from src.bot import BotDispatcher
from src.vectorstore import DocumentIndexer
from src.api import app


class Application:
    """Main application."""

    def __init__(self):
        self.bot = None
        self.indexer = None
        self._initialized = False

    async def startup(self):
        """Start all services."""
        if self._initialized:
            logger.warning("Application already initialized, skipping startup")
            return

        setup_logging()
        logger.info(f"Starting {settings.app_name}")

        try:
            # Initialize indexer
            logger.info("Initializing document indexer...")
            self.indexer = DocumentIndexer()

            # Index existing documents
            logger.info("Indexing existing documents...")
            await self.indexer.index_all()

            # Start file watching
            logger.info("Starting file watcher...")
            self.indexer.start_watching()

            # Initialize and start bot
            logger.info("Starting Telegram bot...")
            self.bot = BotDispatcher()
            self.bot.setup()
            await self.bot.start()

            self._initialized = True
            logger.info("All services started successfully")

        except Exception as e:
            logger.error(f"Startup failed: {e}")
            raise

    async def shutdown(self):
        """Stop all services."""
        if not self._initialized:
            logger.warning("Application not initialized, skipping shutdown")
            return

        logger.info("Shutting down...")

        try:
            if self.bot:
                await self.bot.stop()

            if self.indexer:
                self.indexer.stop_watching()

            self._initialized = False
            logger.info("Shutdown complete")

        except Exception as e:
            logger.error(f"Shutdown error: {e}")


app_instance = Application()


@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager."""
    await app_instance.startup()
    yield
    await app_instance.shutdown()


# Update app with lifespan
app.router.lifespan_context = lifespan


def main():
    """Run application."""
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
