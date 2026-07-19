"""
Command parser for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.commands.models import Command
from assistant.commands.exceptions import CommandParseError

class CommandParser:
    """
    Converts raw text into a Command object.
    """

    def parse(
        self,
        text: str,
    ) -> Command:
        """
        Parse user input into a Command.
        """

        text = text.strip().lower()

        parts = text.split()

        if not parts:
            raise CommandParseError(
                "Command cannot be empty."
            )

        action = parts[0]

        target = None
        arguments = []

        if len(parts) >= 2:
            target = parts[1]

        if len(parts) >= 3:
            arguments = parts[2:]

        return Command(
            action=action,
            target=target,
            arguments=arguments,
        )