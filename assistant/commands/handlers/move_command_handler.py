"""
Handler for the 'move' command.
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


class MoveCommandHandler(
    BaseCommandHandler,
):
    """
    Handles move commands.
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
        Execute the move command.
        """

        self.require_target(
            command,
            "move <file|folder> <source> to <destination>",
        )

        if command.target == "file":
            self._move_file(
                command,
            )
            return

        if command.target == "folder":
            self._move_folder(
                command,
            )
            return

        raise InvalidCommandUsageError(
            "Supported move targets are: file, folder."
        )

    def _move_file(
        self,
        command: Command,
    ) -> None:
        """
        Move a file.
        """

        source_name, destination_folder_name = (
            self._get_names(
                command,
                "file",
            )
        )

        self._move(
            source_name,
            destination_folder_name,
            expected_directory=False,
        )

    def _move_folder(
        self,
        command: Command,
    ) -> None:
        """
        Move a folder.
        """

        source_name, destination_folder_name = (
            self._get_names(
                command,
                "folder",
            )
        )

        self._move(
            source_name,
            destination_folder_name,
            expected_directory=True,
        )

    def _get_names(
        self,
        command: Command,
        item_type: str,
    ) -> tuple[str, str]:
        """
        Extract source name and destination folder name.
        """

        arguments = command.arguments

        if len(arguments) < 3:
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        try:
            separator_index = arguments.index(
                "to"
            )

        except ValueError:
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        if separator_index == 0:
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        if separator_index == len(arguments) - 1:
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        source_name = " ".join(
            arguments[:separator_index]
        )

        destination_folder_name = " ".join(
            arguments[separator_index + 1:]
        )

        if not source_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        if not destination_folder_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: move {item_type} "
                f"<source> to <destination_folder>"
            )

        return (
            source_name,
            destination_folder_name,
        )

    def _move(
        self,
        source_name: str,
        destination_folder_name: str,
        expected_directory: bool,
    ) -> None:
        """
        Find the requested item and move it
        into the destination folder.
        """

        self._logger.info(
            "Searching for '%s' before move.",
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

        self._logger.info(
            "Searching for destination folder '%s'.",
            destination_folder_name,
        )

        destination_folders = (
            self._file_manager.find_directories(
                destination_folder_name,
            )
        )

        if not destination_folders:

            print(
                f"\nCould not find destination folder "
                f"'{destination_folder_name}'.\n"
            )
            return

        if len(destination_folders) > 1:

            print(
                f"\nMultiple destination folders found "
                f"for '{destination_folder_name}'. Please "
                f"use a more specific name.\n"
            )
            return

        destination_folder = destination_folders[0].path

        destination = (
            destination_folder / source.name
        )

        if destination.exists():

            print(
                f"\nCannot move because "
                f"'{destination}' already exists.\n"
            )
            return

        self._logger.info(
            "Moving '%s' to '%s'.",
            source,
            destination,
        )

        moved = self._file_manager.move(
            source,
            destination,
        )

        if moved:
            print(
                f"\nMoved '{source.name}' "
                f"to '{destination_folder}'.\n"
            )
            return

        print(
            f"\nFailed to move "
            f"'{source.name}'.\n"
        )