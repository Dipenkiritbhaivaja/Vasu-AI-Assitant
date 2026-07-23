"""
Handler for opening files.
"""

from __future__ import annotations

from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager
from assistant.files.manager import FileManager
from assistant.files.service import FileService


class OpenFileHandler(BaseCommandHandler):
    """
    Opens a file.
    """

    def __init__(
        self,
        file_manager: FileManager,
        file_service: FileService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._file_manager = file_manager
        self._file_service = file_service

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the open file command.
        """

        if command.target is None:
            raise ValueError(
                "Usage: open file <name>"
            )

        file = self._file_manager.find_best_match(
            command.target
        )

        if file is None:
            print(
                f"File '{command.target}' not found."
            )
            return

        self._file_service.open(file)