"""Custom exceptions."""


class ChatbotException(Exception):
    """Base exception."""
    pass


class DocumentProcessingError(ChatbotException):
    """Document processing failed."""
    pass


class VectorDBError(ChatbotException):
    """Vector database error."""
    pass


class LLMError(ChatbotException):
    """LLM service error."""
    pass


class ConfigurationError(ChatbotException):
    """Configuration error."""
    pass
