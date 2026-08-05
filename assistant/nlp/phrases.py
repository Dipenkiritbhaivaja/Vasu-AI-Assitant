"""
Multi-word phrase normalization.
"""

PHRASES: dict[str, str] = {
    # Search
    "look up": "search",
    "search for": "search",

    # Open
    "bring up": "open",

    # System
    "turn off": "shutdown",
    "power off": "shutdown",
    "sign out": "logoff",
}