"""
Handler for listing registered applications.
"""

from __future__ import annotations

from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.models import (
    Command,
)


class ListApplicationsHandler(
    BaseCommandHandler
):
    """
    Lists all registered applications.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
    ) -> None:

        self._application_manager = (
            application_manager
        )

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        List all registered applications.
        """

        # Validate command usage
        if command.target not in (
            None,
            "applications",
        ):
            raise ValueError(
                "Usage: list applications"
            )

        applications = (
            self._application_manager.get_all()
        )

        print()

        print("Registered Applications")
        print("-----------------------")

        for application in applications:
            print(
                f"• {application.name}"
            )

        print()