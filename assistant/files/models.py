"""
Models for the File module.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FileInfo:
    """
    Represents a file or directory.
    """

    name: str
    path: Path
    is_directory: bool