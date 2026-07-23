"""
Command routing key.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommandKey:
    """
    Unique key used to route commands.
    """

    action: str
    resource: str | None