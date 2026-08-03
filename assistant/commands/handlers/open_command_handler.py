"""
Handler for the 'open' command.
"""

from __future__ import annotations

from assistant.applications.service import ApplicationService

from assistant.applications.manager import ApplicationManager
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager
from assistant.browser.service import BrowserService
from assistant.commands.exceptions import InvalidCommandUsageError
from assistant.applications.exceptions import (
    ApplicationNotFoundError,
)
from assistant.applications.resolver import (
    ApplicationResolver,
)
from assistant.files.manager import (
    FileManager,
)

class OpenCommandHandler(BaseCommandHandler):
    """
    Handles opening applications.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
        browser_service: BrowserService,
        file_manager: FileManager,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )
        self._application_resolver = (
            ApplicationResolver(
                application_manager,
            )
        )
        self._application_service = application_service
        self._browser_service = browser_service
        self._file_manager = file_manager

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the open command.
        """

        target = self.require_target(
            command,
            "open <application>",
        )

        try:
            result = (
                self._application_resolver.resolve(
                    target,
                )
            )

            if self._application_service.is_running(
                result.value
            ):
                print(
                    f"\nApplication '{result.value.name}' is already running.\n"
                )
                return

            self._logger.info(
                "Opening application '%s'.",
                result.value.name,
            )

            if result.kind == "application":
                self._application_service.launch(
                    result.value,
                )
                return

            raise RuntimeError(
                f"Unsupported open target: {result.kind}"
            )

        except ApplicationNotFoundError:

            file = self._file_manager.find_best_match(
                target,
            )

            if file is not None:

                self._logger.info(
                    "Opening file '%s'.",
                    file.path,
                )

                self._file_manager._file_service.open(
                    file,
                )

                return

            self._browser_service.open_url(
                target,
            )