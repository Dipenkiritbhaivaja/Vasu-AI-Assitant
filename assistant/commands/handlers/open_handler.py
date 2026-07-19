"""
Handler for the 'open' command.
"""

from __future__ import annotations

import subprocess

from assistant.applications.manager import ApplicationManager
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager


class OpenApplicationHandler(BaseCommandHandler):
    """
    Handles opening applications.
    """

    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._application_manager = ApplicationManager(
            "data/applications.json"
        )

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

        application = self._application_manager.find(
            command.target
        )

        self._logger.info(
            "Opening application '%s'.",
            application.name,
        )

        subprocess.Popen(
            [application.executable]
        )