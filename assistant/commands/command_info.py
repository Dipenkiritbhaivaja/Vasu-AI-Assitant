"""
Metadata for a registered command.
"""

from __future__ import annotations

from dataclasses import dataclass

from assistant.commands.handlers.base import (
    BaseCommandHandler,
)


@dataclass(slots=True)
class CommandInfo:
    """
    Represents a registered command.
    """

    handler: BaseCommandHandler
    usage: str
    description: str