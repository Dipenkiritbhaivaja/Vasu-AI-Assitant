"""
Console interface for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.commands.manager import CommandManager
from assistant.core.logger import LoggerManager
from assistant.commands.exceptions import (
    CommandHandlerError,
    CommandParseError,
)
from assistant.applications.exceptions import (
    ApplicationNotFoundError,
)

class ConsoleInterface:
    """
    Console-based interface for interacting
    with VASU AI ASSISTANT.
    """

    def __init__(
        self,
        command_manager: CommandManager,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._command_manager = command_manager

    def run(self) -> None:
        """
        Start the interactive console.
        """

        self._logger.info(
            "Console interface started."
        )

        while True:

            command = input("VASU > ").strip()

            if not command:
                continue

            if command.lower() in {
                "exit",
                "quit",
            }:
                print("Goodbye!")
                break

            try:
                self._command_manager.execute(
                    command
                )

            except (
                CommandParseError,
                CommandHandlerError,
                ApplicationNotFoundError,
            ) as error:
                print(error)

            except Exception:
                self._logger.exception(
                    "Unexpected error while executing command."
                )

        self._logger.info(
            "Console interface stopped."
        )