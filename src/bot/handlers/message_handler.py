"""Message handlers."""

from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

from src.services.knowledge import Retriever
from src.services.memory import ConversationMemory


class MessageHandler:
    """Handle user messages."""
    
    def __init__(self):
        self.retriever = Retriever()
        self.memory = ConversationMemory()
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text message."""
        try:
            user_id = update.effective_user.id
            question = update.message.text
            
            logger.info(f"User {user_id}: {question}")
            
            # Send typing indicator
            await update.message.chat.send_action("typing")
            
            # Add to memory
            self.memory.add_message(user_id, "user", question)
            
            # Get answer
            answer, sources, confidence = await self.retriever.retrieve_and_answer(question)
            
            # Add to memory
            self.memory.add_message(user_id, "assistant", answer)
            
            # Format response
            response = answer
            if sources:
                sources_text = "\n".join([f"• {s}" for s in sources])
                response += f"\n\n📚 Sources:\n{sources_text}"
                response += f"\n\n✓ Confidence: {confidence:.0%}"
            
            await update.message.reply_text(response)
            logger.info(f"Answered user {user_id}")
            
        except Exception as e:
            logger.error(f"Message handling error: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error processing your question. Please try again."
            )
