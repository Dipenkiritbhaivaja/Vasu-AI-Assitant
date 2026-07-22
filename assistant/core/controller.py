"""
Application Controller for VASU AI ASSISTANT.

Responsible for coordinating application startup,
shutdown, and shared resources.
"""

from __future__ import annotations
from assistant.applications.manager import ApplicationManager
from assistant.commands.manager import CommandManager
from assistant.core.config import ConfigurationManager
from assistant.core.logger import LoggerManager
from assistant.applications.service import ApplicationService
from assistant.interfaces.console import (
    ConsoleInterface,
)
from assistant.browser.service import BrowserService

class ApplicationController:
    """
    Coordinates the application lifecycle.
    """

    def __init__(self) -> None:
        self.logger = LoggerManager.get_logger(self.__class__.__name__)

        # Shared configuration for the whole application
        self.config: ConfigurationManager = ConfigurationManager()

        self.application_manager: ApplicationManager = ApplicationManager(
            "data/applications.json"
        )

        self.application_service = ApplicationService()
        self.browser_service = BrowserService()

        self.command_manager: CommandManager = CommandManager(
            self.application_manager,
            self.application_service,
            self.browser_service,
        )

        self.console = ConsoleInterface(
            self.command_manager,
        )

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

    def run(self) -> None:
        self.start()

        try:
            self.console.run()
        finally:
            self.stop()