"""
Application Controller for VASU AI ASSISTANT.

Responsible for coordinating application startup,
shutdown, and shared resources.
"""

from __future__ import annotations

from assistant.core.config import ConfigurationManager
from assistant.core.logger import LoggerManager


class ApplicationController:
    """
    Coordinates the application lifecycle.
    """

    def __init__(self) -> None:
        self.logger = LoggerManager.get_logger(self.__class__.__name__)

        # Shared configuration for the whole application
        self.config = ConfigurationManager()

    def start(self) -> None:
        """
        Start the application.
        """
        self.logger.info("Starting VASU AI ASSISTANT...")

    def stop(self) -> None:
        """
        Stop the application.
        """
        self.logger.info("Stopping VASU AI ASSISTANT...")