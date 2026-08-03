"""
Base class for all command handlers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from assistant.commands.exceptions import (
    InvalidCommandUsageError,
)
from assistant.commands.models import Command


class BaseCommandHandler(ABC):
    """
    Base class for all command handlers.
    """

    @abstractmethod
    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute a command.
        """

    def require_target(
        self,
        command: Command,
        usage: str,
    ) -> str:
        """
        Ensure that a command target is provided.

        Args:
            command: Parsed command.
            usage: Usage message.

        Returns:
            Command target.

        Raises:
            InvalidCommandUsageError:
                If no target was provided.
        """

        if not command.target:
            raise InvalidCommandUsageError(
                f"Usage: {usage}"
            )

        return command.target