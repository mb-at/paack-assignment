import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
import os

def setup_logging(log_file: Optional[str] = None, level: Optional[str] = None) -> None:
    """
    Configure logging to output to the console and, optionally, to a file.
    - log_file: Path to the file where logs will be saved. If None, a FileHandler is not created.
    - level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR"). If None, it is taken from LOG_LEVEL or the default is "INFO".
    """

    log_level = level.upper() if level else None
    if log_level is None:
        log_level = (os.getenv("LOG_LEVEL") or "INFO").upper()

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)

    if log_file:
        file_handler = RotatingFileHandler(
            filename=log_file,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        # If the file handler already added does not exist, (avoid duplication)
        if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
            root_logger.addHandler(file_handler)
