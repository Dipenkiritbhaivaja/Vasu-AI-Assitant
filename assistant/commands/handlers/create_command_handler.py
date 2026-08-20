"""
Handler for the 'create' command.
"""

from __future__ import annotations

from pathlib import Path

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
            "create <folder|file> <name> [in <destination>]",
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

        name, destination = self._parse_arguments(
            command,
            "folder",
        )

        self._logger.info(
            "Creating folder '%s'.",
            name,
        )

        if destination is not None:
            self._logger.info(
                "Creating folder in '%s'.",
                destination,
            )

        created = self._file_manager.create_folder(
            name,
            destination,
        )

        if created:
            if destination is None:
                print(
                    f"\nFolder '{name}' created successfully.\n"
                )
            else:
                print(
                    f"\nFolder '{name}' created successfully "
                    f"in '{destination}'.\n"
                )

            return

        print(
            f"\nFailed to create folder '{name}'.\n"
        )

    def _create_file(
        self,
        command: Command,
    ) -> None:
        """
        Create a file.
        """

        name, destination = self._parse_arguments(
            command,
            "file",
        )

        self._logger.info(
            "Creating file '%s'.",
            name,
        )

        if destination is not None:
            self._logger.info(
                "Creating file in '%s'.",
                destination,
            )

        created = self._file_manager.create_file(
            name,
            destination,
        )

        if created:
            if destination is None:
                print(
                    f"\nFile '{name}' created successfully.\n"
                )
            else:
                print(
                    f"\nFile '{name}' created successfully "
                    f"in '{destination}'.\n"
                )

            return

        print(
            f"\nFailed to create file '{name}'.\n"
        )

    def _parse_arguments(
        self,
        command: Command,
        item_type: str,
    ) -> tuple[str, Path | None]:
        """
        Parse the item name and optional destination.

        Supported syntax:

            create file <name>

            create file <name> in <destination>

            create folder <name>

            create folder <name> in <destination>
        """

        arguments = command.arguments

        if not arguments:
            raise InvalidCommandUsageError(
                f"Usage: create {item_type} "
                f"<name> [in <destination>]"
            )

        try:
            separator_index = arguments.index(
                "in"
            )

        except ValueError:
            name = " ".join(
                arguments
            )

            return name, None

        if separator_index == 0:
            raise InvalidCommandUsageError(
                f"Usage: create {item_type} "
                f"<name> [in <destination>]"
            )

        if separator_index == len(arguments) - 1:
            raise InvalidCommandUsageError(
                f"Usage: create {item_type} "
                f"<name> [in <destination>]"
            )

        name = " ".join(
            arguments[:separator_index]
        )

        destination_name = " ".join(
            arguments[separator_index + 1:]
        )

        if not name.strip():
            raise InvalidCommandUsageError(
                f"Usage: create {item_type} "
                f"<name> [in <destination>]"
            )

        if not destination_name.strip():
            raise InvalidCommandUsageError(
                f"Usage: create {item_type} "
                f"<name> [in <destination>]"
            )

        destination = self._file_manager.resolve_directory(
            destination_name,
        )

        if destination is None:
            print(
                f"\nCould not find destination "
                f"directory '{destination_name}'.\n"
            )

            return name, None

        return name, destination