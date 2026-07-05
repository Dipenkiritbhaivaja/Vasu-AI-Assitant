"""
Configuration Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from assistant.core.logger import LoggerManager


class ConfigurationManager:
    """
    Loads and provides access to application settings.
    """

    def __init__(self, config_path: str = "data/settings.json") -> None:
        self.logger = LoggerManager.get_logger(self.__class__.__name__)
        self.config_path = Path(config_path)
        self._settings: dict[str, Any] = {}

        self.load()

    def load(self) -> None:
        """
        Load configuration from the JSON file.
        """

        try:
            if not self.config_path.exists():
                raise FileNotFoundError(
                    f"Configuration file not found: {self.config_path}"
                )

            with self.config_path.open("r", encoding="utf-8") as file:
                self._settings = json.load(file)

            self.logger.info("Configuration loaded successfully.")

        except Exception as error:
            self.logger.exception("Failed to load configuration.")
            raise error
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value using dot notation.

        Example:
            config.get("assistant.name")
        """

        value = self._settings

        for part in key.split("."):
            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value