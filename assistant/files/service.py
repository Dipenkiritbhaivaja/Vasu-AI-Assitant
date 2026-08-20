"""
File Service for VASU AI ASSISTANT.

Responsible for interacting with the file system.
"""

from __future__ import annotations

from pathlib import Path
import os
import shutil

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
        destination: Path | None = None,
    ) -> bool:
        """
        Create a folder.

        Args:
            name: Folder name.
            destination: Directory where the folder should be created.
                Defaults to the current working directory.

        Returns:
            True if the folder was created successfully,
            otherwise False.
        """

        folder_name = name.strip()

        if not folder_name:
            self._logger.warning(
                "Folder name is empty."
            )
            return False

        if destination is None:
            destination = Path.cwd()

        folder_path = destination / folder_name

        if folder_path.exists():
            self._logger.warning(
                "Folder '%s' already exists.",
                folder_path,
            )
            return False

        try:
            folder_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            folder_path.mkdir(
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
        destination: Path | None = None,
    ) -> bool:
        """
        Create an empty file.

        Args:
            name: File name.
            destination: Directory where the file should be created.
                Defaults to the current working directory.

        Returns:
            True if the file was created successfully,
            otherwise False.
        """

        file_name = name.strip()

        if not file_name:
            self._logger.warning(
                "File name is empty."
            )
            return False

        if destination is None:
            destination = Path.cwd()

        file_path = destination / file_name

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


    def delete(
        self,
        path: Path,
    ) -> bool:
        """
        Delete a file or an empty directory.

        Args:
            path: File or directory to delete.

        Returns:
            True if the item was deleted successfully,
            otherwise False.
        """

        if not path.exists():
            self._logger.warning(
                "Cannot delete '%s': item does not exist.",
                path,
            )
            return False

        try:

            if path.is_dir():

                path.rmdir()

                self._logger.info(
                    "Directory deleted successfully: '%s'.",
                    path,
                )

            else:

                path.unlink()

                self._logger.info(
                    "File deleted successfully: '%s'.",
                    path,
                )

            return True

        except OSError as error:

            self._logger.exception(
                "Failed to delete '%s'.",
                path,
                exc_info=error,
            )

            return False

    def rename(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """
        Rename a file or directory.

        Args:
            source: Existing file or directory.
            destination: New file or directory path.

        Returns:
            True if the item was renamed successfully,
            otherwise False.
        """

        if not source.exists():
            self._logger.warning(
                "Cannot rename '%s': item does not exist.",
                source,
            )
            return False

        if destination.exists():
            self._logger.warning(
                "Cannot rename '%s': destination '%s' already exists.",
                source,
                destination,
            )
            return False

        try:
            source.rename(
                destination,
            )

            self._logger.info(
                "Renamed '%s' to '%s'.",
                source,
                destination,
            )

            return True

        except OSError as error:
            self._logger.exception(
                "Failed to rename '%s' to '%s'.",
                source,
                destination,
                exc_info=error,
            )

            return False

    def copy(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """
        Copy a file or directory.

        Args:
            source: Existing file or directory.
            destination: Destination file or directory path.

        Returns:
            True if the item was copied successfully,
            otherwise False.
        """

        if not source.exists():
            self._logger.warning(
                "Cannot copy '%s': item does not exist.",
                source,
            )
            return False

        if destination.exists():
            self._logger.warning(
                "Cannot copy '%s': destination '%s' already exists.",
                source,
                destination,
            )
            return False

        try:

            if source.is_dir():

                shutil.copytree(
                    source,
                    destination,
                )

                self._logger.info(
                    "Directory copied successfully: '%s' to '%s'.",
                    source,
                    destination,
                )

            else:

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.copy2(
                    source,
                    destination,
                )

                self._logger.info(
                    "File copied successfully: '%s' to '%s'.",
                    source,
                    destination,
                )

            return True

        except OSError as error:

            self._logger.exception(
                "Failed to copy '%s' to '%s'.",
                source,
                destination,
                exc_info=error,
            )

            return False

    def move(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """
        Move a file or directory.

        Args:
            source: Existing file or directory.
            destination: Destination file or directory path.

        Returns:
            True if the item was moved successfully,
            otherwise False.
        """

        if not source.exists():
            self._logger.warning(
                "Cannot move '%s': item does not exist.",
                source,
            )
            return False

        if destination.exists():
            self._logger.warning(
                "Cannot move '%s': destination '%s' already exists.",
                source,
                destination,
            )
            return False

        try:

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(source),
                str(destination),
            )

            self._logger.info(
                "Moved '%s' to '%s'.",
                source,
                destination,
            )

            return True

        except OSError as error:

            self._logger.exception(
                "Failed to move '%s' to '%s'.",
                source,
                destination,
                exc_info=error,
            )

            return False