"""
Application Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

import json
from pathlib import Path

from assistant.applications.models import Application
from assistant.applications.exceptions import (
    ApplicationNotFoundError,
)
from assistant.core.logger import LoggerManager


class ApplicationManager:
    """
    Loads and provides access to registered applications.
    """

    def __init__(
        self,
        json_path: str,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._applications: dict[str, Application] = {}

        self._load(json_path)

    def _load(
        self,
        json_path: str,
    ) -> None:
        """
        Load all applications from JSON.
        """

        with open(
            Path(json_path),
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        for item in data["applications"]:

            application = Application(
                name=item["name"],
                executable=item["executable"],
                aliases=item["aliases"],
            )

            self._applications[
                application.name
            ] = application

        self._logger.info(
            "Loaded %d applications.",
            len(self._applications),
        )

    def find(
        self,
        name: str,
    ) -> Application:
        """
        Find an application by name or alias.
        """

        name = name.lower()

        for application in self._applications.values():

            if application.name == name:
                return application

            if name in application.aliases:
                return application

        raise ApplicationNotFoundError(
            f"Application '{name}' is not registered."
        )