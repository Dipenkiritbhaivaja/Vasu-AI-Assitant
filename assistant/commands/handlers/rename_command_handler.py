"""
Handler for the 'rename' command.
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


class RenameCommandHandler(
    BaseCommandHandler,
):
    """
    Handles rename commands.
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
        Execute the rename command.
        """

        self.require_target(
            command,
            "rename <file|folder> <old_name> to <new_name>",
        )

        if command.target == "file":
            self._rename_file(
                command,
            )
            return

        if command.target == "folder":
            self._rename_folder(
                command,
            )
            return

        raise InvalidCommandUsageError(
            "Supported rename targets are: file, folder."
        )

    def _rename_file(
        self,
        command: Command,
    ) -> None:
        """
        Rename a file.
        """

        source_name, destination_name = (
            self._get_names(
                command,
                "file",
            )
        )

        self._rename(
            source_name,
            destination_name,
            expected_directory=False,
        )

    def _rename_folder(
        self,
        command: Command,
    ) -> None:
        """
        Rename a folder.
        """

        source_name, destination_name = (
            self._get_names(
                command,
                "folder",
            )
        )

        self._rename(
            source_name,
            destination_name,
            expected_directory=True,
        )

    def _get_names(
        self,
        command: Command,
        item_type: str,
    ) -> tuple[str, str]:
        """
        Extract source and destination names.
        """

        arguments = command.arguments

        if len(arguments) < 3:
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        try:
            separator_index = arguments.index(
                "to"
            )

        except ValueError:
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        if separator_index == 0:
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        if separator_index == len(arguments) - 1:
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        source_name = " ".join(
            arguments[:separator_index]
        )

        destination_name = " ".join(
            arguments[separator_index + 1:]
        )

        if not source_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        if not destination_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: rename {item_type} "
                f"<old_name> to <new_name>"
            )

        return (
            source_name,
            destination_name,
        )

    def _rename(
        self,
        source_name: str,
        destination_name: str,
        expected_directory: bool,
    ) -> None:
        """
        Find and rename the requested file or folder.
        """

        self._logger.info(
            "Searching for '%s' before rename.",
            source_name,
        )

        results = self._file_manager.search(
            source_name,
        )

        matching_items = [
            item
            for item in results
            if item.is_directory == expected_directory
            and item.name.lower() == source_name.lower()
        ]

        if not matching_items:
            item_type = (
                "folder"
                if expected_directory
                else "file"
            )

            print(
                f"\nCould not find {item_type} "
                f"'{source_name}'.\n"
            )
            return

        if len(matching_items) > 1:
            item_type = (
                "folder"
                if expected_directory
                else "file"
            )

            print(
                f"\nMultiple matching {item_type}s found "
                f"for '{source_name}'. Please use a more "
                f"specific name.\n"
            )
            return

        source = matching_items[0].path
        destination = source.parent / destination_name

        if destination.exists():
            print(
                f"\nCannot rename because "
                f"'{destination}' already exists.\n"
            )
            return

        self._logger.info(
            "Renaming '%s' to '%s'.",
            source,
            destination,
        )

        renamed = self._file_manager.rename(
            source,
            destination,
        )

        if renamed:
            print(
                f"\nRenamed '{source.name}' "
                f"to '{destination.name}'.\n"
            )
            return

        print(
            f"\nFailed to rename "
            f"'{source.name}'.\n"
        )