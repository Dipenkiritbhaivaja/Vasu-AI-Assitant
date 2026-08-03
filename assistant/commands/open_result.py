"""
Models used by the Open command.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class OpenResult:
    """
    Result returned by OpenResolver.
    """

    kind: str
    value: Any