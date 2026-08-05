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

    def create_folder(
        self,
        name: str,
    ) -> bool:
        """
        Create a folder in the current working directory.

        Args:
            name: Name of the folder.

        Returns:
            True if the folder was created successfully,
            False otherwise.
        """

        folder_name = name.strip()

        if not folder_name:
            self._logger.warning(
                "Folder name is empty."
            )
            return False

        folder_path = Path.cwd() / folder_name

        if folder_path.exists():
            self._logger.warning(
                "Folder '%s' already exists.",
                folder_path,
            )
            return False

        try:
            folder_path.mkdir(
                parents=True,
                exist_ok=False,
            )

            self._logger.info(
                "Folder created successfully: '%s'.",
                folder_path,
            )

            return True

        except OSError as error:
            self._logger.exception(
                "Failed to create folder '%s'.",
                folder_path,
                exc_info=error,
            )

            return False

    def create_file(
        self,
        name: str,
    ) -> bool:
        """
        Create an empty file in the current
        working directory.

        Args:
            name: File name.

        Returns:
            True if the file was created
            successfully, otherwise False.
        """

        file_name = name.strip()

        if not file_name:
            self._logger.warning(
                "File name is empty."
            )
            return False

        file_path = Path.cwd() / file_name

        if file_path.exists():
            self._logger.warning(
                "File '%s' already exists.",
                file_path,
            )
            return False

        try:
            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.touch(
                exist_ok=False,
            )

            self._logger.info(
                "File created successfully: '%s'.",
                file_path,
            )

            return True

        except OSError as error:
            self._logger.exception(
                "Failed to create file '%s'.",
                file_path,
                exc_info=error,
            )

            return False