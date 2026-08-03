"""
Handler for the 'search' command.
"""

from __future__ import annotations

from assistant.browser.service import BrowserService
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager


class SearchCommandHandler(BaseCommandHandler):
    """
    Handles Google searches.
    """

    def __init__(
        self,
        browser_service: BrowserService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._browser_service = browser_service

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute the search command.
        """

        target = self.require_target(
            command,
            "search <query>",
        )

        query = command.text

        self._logger.info(
            "Searching Google for '%s'.",
            query,
        )

        self._browser_service.search(
            query,
        )