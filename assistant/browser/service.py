"""
Browser Service for VASU AI ASSISTANT.
"""

from __future__ import annotations

import webbrowser

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