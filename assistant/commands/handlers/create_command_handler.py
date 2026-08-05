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

        if command.target == "folder":
            self._create_folder(
                command,
            )
            return

        if command.target == "file":
            self._create_file(
                command,
            )
            return

        raise InvalidCommandUsageError(
            "Supported create targets are: folder, file."
        )

    def _create_folder(
        self,
        command: Command,
    ) -> None:
        """
        Create a folder.
        """

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

    def _create_file(
        self,
        command: Command,
    ) -> None:
        """
        Create a file.
        """

        if not command.arguments:
            raise InvalidCommandUsageError(
                "Usage: create file <file_name>"
            )

        file_name = " ".join(
            command.arguments
        )

        self._logger.info(
            "Creating file '%s'.",
            file_name,
        )

        created = self._file_manager.create_file(
            file_name,
        )

        if created:
            print(
                f"\nFile '{file_name}' created successfully.\n"
            )
            return

        print(
            f"\nFailed to create file '{file_name}'.\n"
        )