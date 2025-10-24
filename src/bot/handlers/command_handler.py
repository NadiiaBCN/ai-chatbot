"""Command handlers."""

from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

from src.core import settings
from src.vectorstore import PineconeStore


class CommandHandler:
    """Handle bot commands."""
    
    def __init__(self):
        self.vectorstore = PineconeStore()
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        message = """
👋 Welcome to AI Knowledge Base Bot!

I can answer questions based on our document library.

Just send me your question and I'll search for the answer!

Commands:
/help - Show help
/status - Check bot status
"""
        await update.message.reply_text(message)
        logger.info(f"User {update.effective_user.id} started bot")
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        message = """
📖 How to use this bot:

1. Send your question as a message
2. I'll search our knowledge base
3. You'll receive an answer with sources

Example:
"What are healthy eating tips?"

Tips:
• Be specific in your questions
• Ask one question at a time
• Use /status to check if I'm working properly
"""
        await update.message.reply_text(message)
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        try:
            connected = self.vectorstore.is_connected()
            
            status_emoji = "✅" if connected else "❌"
            status_text = "Online" if connected else "Offline"
            
            message = f"""
🤖 Bot Status

Vector Database: {status_emoji} {status_text}
Version: 1.0.0

{'✓ Ready to answer questions!' if connected else '⚠ Experiencing connectivity issues'}
"""
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            await update.message.reply_text("Error checking status")
