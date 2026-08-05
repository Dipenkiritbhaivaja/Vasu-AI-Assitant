from __future__ import annotations

import re


class IntentMatcher:
    """
    Detects command intent from natural language.
    """

    PATTERNS = {
        "open": [
            r"\bopen\b",
            r"\blaunch\b",
            r"\bstart\b",
            r"\brun\b",
            r"\bbring up\b",
        ],
        "close": [
            r"\bclose\b",
            r"\bexit\b",
            r"\bquit\b",
            r"\bterminate\b",
        ],
        "find": [
            r"\bfind\b",
            r"\blocate\b",
            r"\bsearch for file\b",
        ],
        "search": [
            r"\bgoogle\b",
            r"\bsearch\b",
            r"\blook up\b",
        ],
        "play": [
            r"\bplay\b",
        ],
    }

    @classmethod
    def detect(cls, text: str) -> str | None:
        lowered = text.lower()

        for command, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, lowered):
                    return command

        return None