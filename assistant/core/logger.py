"""
Centralized logging configuration for VASU AI ASSISTANT.

Every module in the application should obtain its logger
through LoggerManager instead of creating its own logging
configuration.
"""

from __future__ import annotations

import logging
from pathlib import Path


class LoggerManager:
    """
    Creates and manages application loggers.

    This class ensures the logging configuration
    is created only once.
    """

    _configured = False

    @classmethod
    def configure(cls) -> None:
        """
        Configure the root logger.

        Safe to call multiple times.
        """

        if cls._configured:
            return

        log_directory = Path("logs")
        log_directory.mkdir(exist_ok=True)

        log_file = log_directory / "vasu_ai.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Return a configured logger.

        Args:
            name: Module name.

        Returns:
            logging.Logger
        """

        cls.configure()

        return logging.getLogger(name)