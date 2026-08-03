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
    target: str | None = None
    arguments: list[str] = field(default_factory=list)

    @property
    def text(
        self,
    ) -> str:
        """
        Return the full target text.

        Example:
            search python decorators
            -> "python decorators"
        """

        if self.target is None:
            return ""

        return " ".join(
            [
                self.target,
                *self.arguments,
            ]
        )