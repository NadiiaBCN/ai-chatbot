"""Logging configuration."""

import sys
from loguru import logger
from pathlib import Path
from src.core.config import settings


def setup_logging():
    """Configure application logging."""
    logger.remove()
    
    # Console logging
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File logging
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        level=settings.log_level,
    )
    
    logger.add(
        log_path / "error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="90 days",
        compression="zip",
        level="ERROR",
    )
