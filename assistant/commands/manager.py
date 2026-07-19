"""
Command Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.commands.exceptions import (
    CommandHandlerError,
)
from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.handlers.open_handler import (
    OpenApplicationHandler,
)
from assistant.commands.parser import (
    CommandParser,
)
from assistant.core.logger import (
    LoggerManager,
)


class CommandManager:
    """
    Coordinates command parsing and execution.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._parser = CommandParser()

        self._application_manager = application_manager

        self._handlers: dict[
            str,
            BaseCommandHandler,
        ] = {
            "open": OpenApplicationHandler(
                self._application_manager,
            ),
        }

    def execute(
        self,
        text: str,
    ) -> None:
        """
        Parse and execute a command.
        """

        command = self._parser.parse(text)

        handler = self._handlers.get(
            command.action
        )

        if handler is None:
            raise CommandHandlerError(
                f"No handler registered for '{command.action}'."
            )

        self._logger.info(
            "Executing command '%s'.",
            command.action,
        )

        handler.execute(command)