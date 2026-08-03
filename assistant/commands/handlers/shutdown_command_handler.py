"""
Handler for the 'shutdown' command.
"""

from __future__ import annotations

from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.models import (
    Command,
)
from assistant.core.logger import (
    LoggerManager,
)
from assistant.system.service import (
    SystemService,
)


class ShutdownCommandHandler(
    BaseCommandHandler,
):
    """
    Handles the shutdown command.
    """

    def __init__(
        self,
        system_service: SystemService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._system_service = system_service

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the shutdown command.
        """

        self._logger.info(
            "Shutting down system..."
        )

        self._system_service.shutdown()