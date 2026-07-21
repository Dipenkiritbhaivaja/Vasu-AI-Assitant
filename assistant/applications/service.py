"""
Application Service for VASU AI ASSISTANT.

Responsible for interacting with the operating system
to manage registered applications.
"""

from __future__ import annotations

import subprocess
import psutil
from assistant.applications.models import Application
from assistant.core.logger import LoggerManager


class ApplicationService:
    """
    Provides operating system operations
    for registered applications.
    """

    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def launch(
        self,
        application: Application,
    ) -> None:
        """
        Launch an application.

        Args:
            application: Application to launch.
        """

        self._logger.info(
            "Launching application '%s'.",
            application.name,
        )

        subprocess.Popen(
            [application.executable]
        )

    def close(
        self,
        application: Application,
    ) -> None:
        """
        Gracefully close an application.

        Args:
            application: Application to close.
        """

        self._logger.info(
            "Closing application '%s'.",
            application.name,
        )

        for process in psutil.process_iter(
            ["pid", "name"]
        ):

            process_name = (
                process.info["name"] or ""
            ).lower()

            if process_name != application.executable.lower():
                continue

            process.terminate()

            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                self._logger.warning(
                    "Application '%s' did not terminate gracefully. Killing process.",
                    application.name,
                )
                process.kill()

            self._logger.info(
                "Application '%s' closed.",
                application.name,
            )
            return

        self._logger.warning(
            "Application '%s' is not running.",
            application.name,
        )

    def restart(
        self,
        application: Application,
    ) -> None:
        """
        Restart an application.

        Args:
            application: Application to restart.
        """

        self._logger.info(
            "Restarting application '%s'.",
            application.name,
        )

        self.close(application)

        self.launch(application)