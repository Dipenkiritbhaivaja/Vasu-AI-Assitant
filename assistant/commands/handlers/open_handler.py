"""
Handler for the 'open' command.
"""

from __future__ import annotations

from assistant.applications.service import ApplicationService

from assistant.applications.manager import ApplicationManager
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager
from assistant.browser.service import BrowserService

from assistant.applications.exceptions import (
    ApplicationNotFoundError,
)

class OpenApplicationHandler(BaseCommandHandler):
    """
    Handles opening applications.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
        browser_service: BrowserService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )
        self._application_manager = application_manager
        self._application_service = application_service
        self._browser_service = browser_service

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the open command.
        """

        if command.target is None:
            raise ValueError(
                "No application specified."
            )

        try:
            application = self._application_manager.find(
                command.target
            )

            if self._application_service.is_running(
                application
            ):
                print(
                    f"\nApplication '{application.name}' is already running.\n"
                )
                return

            self._logger.info(
                "Opening application '%s'.",
                application.name,
            )

            self._application_service.launch(
                application
            )

        except ApplicationNotFoundError:
            self._browser_service.open_url(
                command.target
            )