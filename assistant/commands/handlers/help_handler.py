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

    def __init__(
        self,
        command_manager,
    ) -> None:

        self._command_manager = command_manager

    def execute(
        self,
        command: Command,
    ) -> None:

        print()

        print("Available Commands")
        print("------------------")

        for info in self._command_manager.get_registered_commands().values():
            print(f"  {info.usage}")

        print()