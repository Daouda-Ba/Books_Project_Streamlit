"""Configuration centralisee du logging."""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Retourne un logger configure de maniere idempotente."""
    level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    log_level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
        )
        logger.addHandler(handler)

    return logger
