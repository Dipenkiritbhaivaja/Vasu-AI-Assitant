"""
Browser Service for VASU AI ASSISTANT.
"""

from __future__ import annotations

import webbrowser
from urllib.parse import quote_plus
from assistant.core.logger import LoggerManager


class BrowserService:
    """
    Provides browser-related operations.
    """

    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def open_url(
        self,
        url: str,
    ) -> None:
        """
        Open a URL in the default browser.
        """

        if not url.startswith(
            (
                "http://",
                "https://",
            )
        ):
            url = f"https://{url}"

        self._logger.info(
            "Opening URL '%s'.",
            url,
        )

        webbrowser.open(url)

    def search(
        self,
        query: str,
    ) -> None:
        """
        Search Google for a query.
        """

        url = (
            "https://www.google.com/search?q="
            f"{quote_plus(query)}"
        )

        self._logger.info(
            "Searching Google for '%s'.",
            query,
        )

        webbrowser.open(url)

    def play(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube for a query.
        """

        url = (
            "https://www.youtube.com/results"
            f"?search_query={quote_plus(query)}"
        )

        self._logger.info(
            "Playing '%s' on YouTube.",
            query,
        )

        webbrowser.open(url)