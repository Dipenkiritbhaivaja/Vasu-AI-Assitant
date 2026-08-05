"""
Handler for the 'create' command.
"""

from __future__ import annotations

from assistant.commands.exceptions import (
    InvalidCommandUsageError,
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
from assistant.files.manager import (
    FileManager,
)


class CreateCommandHandler(
    BaseCommandHandler,
):
    """
    Handles create commands.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._file_manager = file_manager

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the create command.
        """

        self.require_target(
            command,
            "create <folder> <name>",
        )

        if command.target != "folder":
            raise InvalidCommandUsageError(
                "Currently only 'create folder' is supported."
            )

        if not command.arguments:
            raise InvalidCommandUsageError(
                "Usage: create folder <folder_name>"
            )

        folder_name = " ".join(
            command.arguments
        )

        self._logger.info(
            "Creating folder '%s'.",
            folder_name,
        )

        created = self._file_manager.create_folder(
            folder_name,
        )

        if created:
            print(
                f"\nFolder '{folder_name}' created successfully.\n"
            )
            return

        print(
            f"\nFailed to create folder '{folder_name}'.\n"
        )