"""
Models for the System module.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CpuInfo:
    """
    CPU information.
    """

    usage: float
    physical_cores: int
    logical_cores: int
    frequency: float