"""
Handler for the 'play' command.
"""

from __future__ import annotations

from assistant.browser.service import BrowserService
from assistant.commands.handlers.base import BaseCommandHandler
from assistant.commands.models import Command
from assistant.core.logger import LoggerManager


class PlayCommandHandler(BaseCommandHandler):
    """
    Handles YouTube searches.
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
        Execute the play command.
        """

        self.require_target(
            command,
            "play <query>",
        )

        query = command.text

        self._logger.info(
            "Playing '%s'.",
            query,
        )

        self._browser_service.play(
            query,
        )