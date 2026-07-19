"""
Command Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.commands.parser import CommandParser
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.handlers.open_handler import (
    OpenApplicationHandler,
)
from assistant.core.logger import LoggerManager
from assistant.commands.exceptions import (
    CommandHandlerError,
)


class CommandManager:
    """
    Coordinates command parsing and execution.
    """

    def __init__(self) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._parser = CommandParser()

        self._handlers: dict[
            str,
            BaseCommandHandler,
        ] = {
            "open": OpenApplicationHandler(),
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