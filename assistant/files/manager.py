"""
File Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

from pathlib import Path

from assistant.core.logger import LoggerManager
from assistant.files.models import FileInfo
from assistant.files.service import FileService
from assistant.files.search_locations import (
    get_default_locations,
)

class FileManager:
    """
    Coordinates file searching.
    """

    def __init__(
        self,
        file_service: FileService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._file_service = file_service

    def search(
        self,
        name: str,
    ) -> list[FileInfo]:
        """
        Search for a file.
        """

        self._logger.info(
            "Searching for '%s'.",
            name,
        )

        results: list[FileInfo] = []

        for location in get_default_locations():

            if not location.exists():
                continue

            self._logger.info(
                "Searching location: %s",
                location,
            )

            results.extend(
                self._file_service.search(
                    location,
                    name,
                )
            )

        return results

    def find_best_match(
        self,
        name: str,
    ) -> FileInfo | None:
        """
        Return the best matching file.
        """

        results = self.search(name)

        if not results:
            return None

        return results[0]

    def find_directories(
        self,
        name: str,
    ) -> list[FileInfo]:
        """
        Find directories by exact name.

        This also checks the default search locations
        themselves, not only their contents.

        Args:
            name: Directory name.

        Returns:
            List of matching directories.
        """

        self._logger.info(
            "Searching for directory '%s'.",
            name,
        )

        normalized_name = name.strip().lower()

        if not normalized_name:
            return []

        results: list[FileInfo] = []

        for location in get_default_locations():

            if not location.exists():
                continue

            self._logger.info(
                "Checking directory location: %s",
                location,
            )

            if (
                location.is_dir()
                and location.name.lower()
                == normalized_name
            ):
                results.append(
                    FileInfo(
                        name=location.name,
                        path=location,
                        is_directory=True,
                    )
                )

            for path in location.rglob("*"):

                if not path.is_dir():
                    continue

                if (
                    path.name.lower()
                    != normalized_name
                ):
                    continue

                results.append(
                    FileInfo(
                        name=path.name,
                        path=path,
                        is_directory=True,
                    )
                )

        self._logger.info(
            "Found %d matching directory(s).",
            len(results),
        )

        return results

    def create_folder(
        self,
        name: str,
        destination: Path | None = None,
    ) -> bool:
        """
        Create a folder.

        Args:
            name: Folder name.

        Returns:
            True if the folder was created successfully,
            otherwise False.
        """

        self._logger.info(
            "Creating folder '%s'.",
            name,
        )

        return self._file_service.create_folder(
            name,
            destination,
        )

    def create_file(
        self,
        name: str,
        destination: Path | None = None,
    ) -> bool:
        """
        Create a file.

        Args:
            name: File name.

        Returns:
            True if the file was created successfully,
            otherwise False.
        """

        self._logger.info(
            "Creating file '%s'.",
            name,
        )

        return self._file_service.create_file(
            name,
            destination,
        )

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

        self._logger.info(
            "Deleting '%s'.",
            path,
        )

        return self._file_service.delete(
            path,
        )

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

        self._logger.info(
            "Renaming '%s' to '%s'.",
            source,
            destination,
        )

        return self._file_service.rename(
            source,
            destination,
        )

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

        self._logger.info(
            "Copying '%s' to '%s'.",
            source,
            destination,
        )

        return self._file_service.copy(
            source,
            destination,
        )

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

        self._logger.info(
            "Moving '%s' to '%s'.",
            source,
            destination,
        )

        return self._file_service.move(
            source,
            destination,
        )

    def resolve_directory(
        self,
        name: str,
    ) -> Path | None:
        """
        Resolve a directory name to its actual path.

        The directory can be:
        - An absolute path.
        - A directory in the default search locations.
        - A directory inside the current working directory.

        Args:
            name: Directory name or path.

        Returns:
            Resolved directory path, or None if not found.
        """

        directory_name = name.strip()

        if not directory_name:
            return None

        requested_path = Path(directory_name).expanduser()

        if requested_path.is_absolute():
            if requested_path.is_dir():
                return requested_path

            return None

        current_directory = Path.cwd() / directory_name

        if current_directory.is_dir():
            return current_directory

        results = self.find_directories(
            directory_name,
        )

        if len(results) == 1:
            return results[0].path

        if len(results) > 1:
            self._logger.warning(
                "Multiple directories found for '%s'.",
                directory_name,
            )

        return None