"""
Handler for the 'status' command.
"""

from __future__ import annotations

from assistant.applications.manager import ApplicationManager
from assistant.applications.service import ApplicationService
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager


class StatusApplicationHandler(BaseCommandHandler):
    """
    Handles application status requests.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._application_manager = application_manager
        self._application_service = application_service

    def execute(
        self,
        command: Command,
    ) -> None:

        if command.target is None:
            raise ValueError(
                "No application specified."
            )

        application = self._application_manager.find(
            command.target
        )

        running = self._application_service.is_running(
            application
        )

        if running:
            print(
                f"\nApplication '{application.name}' is running.\n"
            )
        else:
            print(
                f"\nApplication '{application.name}' is not running.\n"
            )