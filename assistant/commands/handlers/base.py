"""
Base class for all command handlers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from assistant.commands.models import Command


class BaseCommandHandler(ABC):
    """
    Base class for command handlers.
    """

    @abstractmethod
    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute a command.
        """