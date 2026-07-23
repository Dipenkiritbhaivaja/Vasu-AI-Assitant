"""
Handler for the 'find' command.
"""

from __future__ import annotations

from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager
from assistant.files.manager import FileManager


class FindFileHandler(BaseCommandHandler):
    """
    Handles file searching.
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
        Execute the find command.
        """

        if command.target is None:
            raise ValueError(
                "Usage: find <file_name>"
            )

        results = self._file_manager.search(
            command.target,
        )

        print()

        if not results:
            print(
                f"No file found matching '{command.target}'."
            )
            print()
            return

        print("Search Results")
        print("--------------")

        for file in results:
            print(file.path)

        print()