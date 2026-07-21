"""
Handler for the 'help' command.
"""

from __future__ import annotations

from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.models import (
    Command,
)


class HelpCommandHandler(BaseCommandHandler):
    """
    Displays available commands.
    """

    def execute(
        self,
        command: Command,
    ) -> None:

        print()

        print("Available Commands")
        print("------------------")

        print("Application")
        print("  open <application>")
        print("  close <application>")
        print("  restart <application>")

        print()

        print("General")
        print("  help")
        print("  exit")
        print()