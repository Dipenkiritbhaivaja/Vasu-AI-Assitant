"""
Application models for VASU AI ASSISTANT.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Application:
    """
    Represents a registered application.
    """

    name: str
    executable: str
    process_name: str
    aliases: list[str]
    arguments: list[str] = field(
        default_factory=list
    )
    working_directory: str | None = None
    run_as_admin: bool = False