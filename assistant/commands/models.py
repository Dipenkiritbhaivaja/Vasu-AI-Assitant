"""
Command models for VASU AI ASSISTANT.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Command:
    """
    Represents a parsed command.

    A command is the structured representation of
    user input after parsing, but before execution.
    """

    action: str
    resource: str | None
    target: str | None = None
    arguments: list[str] = field(default_factory=list)