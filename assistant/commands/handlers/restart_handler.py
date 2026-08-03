"""
Handler for the 'restart' command.
"""

from __future__ import annotations

from assistant.applications.manager import ApplicationManager
from assistant.applications.service import ApplicationService
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager
from assistant.system.service import SystemService

class RestartApplicationHandler(BaseCommandHandler):
    """
    Handles restarting applications.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
        system_service: SystemService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._application_manager = application_manager
        self._application_service = application_service
        self._system_service = system_service

    def execute(
        self,
        command: Command,
    ) -> None:

        target = self.require_target(
            command,
            "restart <target>",
        )

        if target.lower() in {
            "pc",
            "computer",
            "system",
        }:
            self._logger.info(
                "Restarting computer."
            )

            self._system_service.restart()

            return
        
        application = self._application_manager.find(
            target,
        )

        self._logger.info(
            "Restarting application '%s'.",
            application.name,
        )

        self._application_service.restart(
            application
        )