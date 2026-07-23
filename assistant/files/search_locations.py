"""
Default search locations for VASU AI ASSISTANT.
"""

from pathlib import Path


def get_default_locations() -> list[Path]:
    """
    Return default search locations.
    """

    home = Path.home()

    locations = [
        home / "Desktop",
        home / "OneDrive" / "Desktop",
        home / "Documents",
        home / "OneDrive" / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "OneDrive" / "Pictures",
        home / "Videos",
        home / "OneDrive" / "Videos",
    ]

    return [
        location
        for location in locations
        if location.exists()
    ]