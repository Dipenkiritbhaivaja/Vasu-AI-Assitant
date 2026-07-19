"""
Application models for VASU AI ASSISTANT.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Application:
    """
    Represents an application that VASU can launch.
    """

    name: str

    executable: str

    aliases: list[str] = field(default_factory=list)