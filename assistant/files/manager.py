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