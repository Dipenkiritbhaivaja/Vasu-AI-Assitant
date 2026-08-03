"""
Audio Service for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.core.logger import LoggerManager


class AudioService:
    """
    Provides audio-related operations.
    """

    def __init__(
        self,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )