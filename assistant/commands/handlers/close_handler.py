"""
Handler for the 'close' command.
"""

from __future__ import annotations

from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.applications.service import (
    ApplicationService,
)
from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.models import (
    Command,
)
from assistant.core.logger import (
    LoggerManager,
)


class CloseApplicationHandler(BaseCommandHandler):
    """
    Handles closing applications.
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

        if not self._application_service.is_running(
            application
        ):
            print(
                f"\nApplication '{application.name}' is already closed.\n"
            )
            return

        self._logger.info(
            "Closing application '%s'.",
            application.name,
        )

        self._application_service.close(
            application
        )