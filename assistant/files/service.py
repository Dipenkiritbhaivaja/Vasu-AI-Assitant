"""
File Service for VASU AI ASSISTANT.

Responsible for interacting with the file system.
"""

from __future__ import annotations

from pathlib import Path
import os
from assistant.core.logger import LoggerManager
from assistant.files.models import FileInfo


class FileService:
    """
    Provides file system operations.
    """

    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def search(
        self,
        root: Path,
        name: str,
    ) -> list[FileInfo]:
        """
        Search for files and directories recursively.

        Args:
            root: Root directory to search.
            name: File or directory name.

        Returns:
            List of matching FileInfo objects.
        """

        self._logger.info(
            "Searching '%s' under '%s'.",
            name,
            root,
        )

        matches: list[FileInfo] = []

        name = name.lower()

        for path in root.rglob("*"):

            if name not in path.name.lower():
                continue

            matches.append(
                FileInfo(
                    name=path.name,
                    path=path,
                    is_directory=path.is_dir(),
                )
            )

        self._logger.info(
            "Found %d matching item(s).",
            len(matches),
        )

        return matches

    def open(
        self,
        file: FileInfo,
    ) -> None:
        """
        Open a file using the operating system.

        Args:
            file: File to open.
        """

        self._logger.info(
            "Opening file '%s'.",
            file.path,
        )

        os.startfile(file.path)