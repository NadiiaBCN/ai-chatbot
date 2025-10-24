"""Telegram bot dispatcher."""

from telegram.ext import Application, CommandHandler as TgCommandHandler, MessageHandler as TgMessageHandler, filters
from loguru import logger

from src.core import settings
from src.bot.handlers import MessageHandler, CommandHandler


class BotDispatcher:
    """Setup and run Telegram bot."""
    
    def __init__(self):
        self.application = None
        self.message_handler = MessageHandler()
        self.command_handler = CommandHandler()
    
    def setup(self):
        """Setup bot handlers."""
        try:
            self.application = Application.builder().token(settings.telegram_bot_token).build()
            
            # Commands
            self.application.add_handler(TgCommandHandler("start", self.command_handler.start))
            self.application.add_handler(TgCommandHandler("help", self.command_handler.help))
            self.application.add_handler(TgCommandHandler("status", self.command_handler.status))
            
            # Messages
            self.application.add_handler(
                TgMessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.handle_text)
            )
            
            logger.info("Bot handlers configured")
            
        except Exception as e:
            logger.error(f"Bot setup failed: {e}")
            raise
    
    async def start(self):
        """Start bot."""
        try:
            logger.info("Starting Telegram bot...")
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(drop_pending_updates=True)
            logger.info("Bot started")
        except Exception as e:
            logger.error(f"Bot start failed: {e}")
            raise
    
    async def stop(self):
        """Stop bot."""
        try:
            if self.application:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                logger.info("Bot stopped")
        except Exception as e:
            logger.error(f"Bot stop error: {e}")
