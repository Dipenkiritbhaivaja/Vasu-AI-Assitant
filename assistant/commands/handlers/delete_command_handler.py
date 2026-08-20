"""
Handler for the 'delete' command.
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


class DeleteCommandHandler(
    BaseCommandHandler,
):
    """
    Handles delete commands.
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
        Execute the delete command.
        """

        self.require_target(
            command,
            "delete <file|folder> <name>",
        )

        if command.target == "file":
            self._delete_file(
                command,
            )
            return

        if command.target == "folder":
            self._delete_folder(
                command,
            )
            return

        raise InvalidCommandUsageError(
            "Supported delete targets are: file, folder."
        )

    def _delete_file(
        self,
        command: Command,
    ) -> None:
        """
        Delete a file.
        """

        if not command.arguments:
            raise InvalidCommandUsageError(
                "Usage: delete file <file_name>"
            )

        file_name = " ".join(
            command.arguments
        )

        self._delete(
            file_name,
            expected_directory=False,
        )

    def _delete_folder(
        self,
        command: Command,
    ) -> None:
        """
        Delete a folder.
        """

        if not command.arguments:
            raise InvalidCommandUsageError(
                "Usage: delete folder <folder_name>"
            )

        folder_name = " ".join(
            command.arguments
        )

        self._delete(
            folder_name,
            expected_directory=True,
        )

    def _delete(
        self,
        name: str,
        expected_directory: bool,
    ) -> None:
        """
        Find and delete the requested file or folder.
        """

        self._logger.info(
            "Searching for '%s' before deletion.",
            name,
        )

        results = self._file_manager.search(
            name,
        )

        if not results:
            print(
                f"\nCould not find '{name}'.\n"
            )
            return

        matching_items = [
            item
            for item in results
            if item.is_directory == expected_directory
        ]

        if not matching_items:
            item_type = (
                "folder"
                if expected_directory
                else "file"
            )

            print(
                f"\nNo {item_type} named '{name}' was found.\n"
            )
            return

        if len(matching_items) > 1:
            print(
                f"\nMultiple matching items found for "
                f"'{name}'. Please use a more specific name.\n"
            )
            return

        item = matching_items[0]

        self._logger.info(
            "Deleting %s '%s'.",
            "folder" if item.is_directory else "file",
            item.path,
        )

        deleted = self._file_manager.delete(
            item.path,
        )

        if deleted:
            print(
                f"\nDeleted '{item.path}'.\n"
            )
            return

        print(
            f"\nFailed to delete '{item.path}'.\n"
        )