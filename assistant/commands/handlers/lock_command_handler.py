"""
Handler for the 'lock' command.
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


class LockCommandHandler(
    BaseCommandHandler,
):
    """
    Handles the lock command.
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
        Execute the lock command.
        """

        self._logger.info(
            "Locking workstation."
        )

        self._system_service.lock()