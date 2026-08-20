"""
Handler for the 'copy' command.
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


class CopyCommandHandler(
    BaseCommandHandler,
):
    """
    Handles copy commands.
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
        Execute the copy command.
        """

        self.require_target(
            command,
            "copy <file|folder> <source> to <destination>",
        )

        if command.target == "file":
            self._copy_file(
                command,
            )
            return

        if command.target == "folder":
            self._copy_folder(
                command,
            )
            return

        raise InvalidCommandUsageError(
            "Supported copy targets are: file, folder."
        )

    def _copy_file(
        self,
        command: Command,
    ) -> None:
        """
        Copy a file.
        """

        source_name, destination_name = (
            self._get_names(
                command,
                "file",
            )
        )

        self._copy(
            source_name,
            destination_name,
            expected_directory=False,
        )

    def _copy_folder(
        self,
        command: Command,
    ) -> None:
        """
        Copy a folder.
        """

        source_name, destination_name = (
            self._get_names(
                command,
                "folder",
            )
        )

        self._copy(
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
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        try:
            separator_index = arguments.index(
                "to"
            )

        except ValueError:
            raise InvalidCommandUsageError(
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        if separator_index == 0:
            raise InvalidCommandUsageError(
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        if separator_index == len(arguments) - 1:
            raise InvalidCommandUsageError(
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        source_name = " ".join(
            arguments[:separator_index]
        )

        destination_name = " ".join(
            arguments[separator_index + 1:]
        )

        if not source_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        if not destination_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: copy {item_type} "
                f"<source> to <destination>"
            )

        return (
            source_name,
            destination_name,
        )

    def _copy(
        self,
        source_name: str,
        destination_name: str,
        expected_directory: bool,
    ) -> None:
        """
        Find and copy the requested file or folder
        to the requested destination.
        """

        self._logger.info(
            "Searching for '%s' before copy.",
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

        # -------------------------------------------------
        # Find destination folder
        # -------------------------------------------------

        self._logger.info(
            "Searching for destination folder '%s'.",
            destination_name,
        )

        destination_results = (
            self._file_manager.find_directories(
                destination_name,
            )
        )

        matching_destinations = [
            item
            for item in destination_results
            if item.name.lower()
            == destination_name.lower()
        ]

        if not matching_destinations:

            print(
                f"\nCould not find destination folder "
                f"'{destination_name}'.\n"
            )
            return

        if len(matching_destinations) > 1:

            print(
                f"\nMultiple destination folders found "
                f"for '{destination_name}'. Please use "
                f"a more specific name.\n"
            )
            return

        destination_folder = (
            matching_destinations[0].path
        )

        destination = (
            destination_folder / source.name
        )

        # -------------------------------------------------
        # Check destination
        # -------------------------------------------------

        if destination.exists():

            print(
                f"\nCannot copy because "
                f"'{destination}' already exists.\n"
            )
            return

        self._logger.info(
            "Copying '%s' to '%s'.",
            source,
            destination,
        )

        copied = self._file_manager.copy(
            source,
            destination,
        )

        if copied:

            print(
                f"\nCopied '{source.name}' "
                f"to '{destination_folder}'.\n"
            )
            return

        print(
            f"\nFailed to copy "
            f"'{source.name}'.\n"
        )