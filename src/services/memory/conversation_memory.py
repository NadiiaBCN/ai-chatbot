"""Conversation memory management."""

from collections import defaultdict
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """Chat message."""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


class ConversationMemory:
    """Store conversation history."""
    
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.conversations: Dict[int, List[Message]] = defaultdict(list)
    
    def add_message(self, user_id: int, role: str, content: str):
        """Add message to history."""
        message = Message(role=role, content=content)
        self.conversations[user_id].append(message)
        
        # Limit history size
        if len(self.conversations[user_id]) > self.max_messages:
            self.conversations[user_id] = self.conversations[user_id][-self.max_messages:]
    
    def get_history(self, user_id: int) -> List[Message]:
        """Get conversation history."""
        return self.conversations[user_id]
    
    def clear_history(self, user_id: int):
        """Clear user history."""
        self.conversations[user_id] = []
