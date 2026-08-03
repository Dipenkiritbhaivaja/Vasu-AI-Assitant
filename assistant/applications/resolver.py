"""
Application Resolver for VASU AI ASSISTANT.

Responsible for resolving application names
from user input.
"""

from __future__ import annotations

from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.applications.models import (
    Application,
)
from assistant.commands.open_result import (
    OpenResult,
)

class ApplicationResolver:
    """
    Resolves application names into
    registered Application objects.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
    ) -> None:
        self._application_manager = (
            application_manager
        )

    def resolve(
        self,
        target: str,
    ) -> OpenResult:
        """
        Resolve a user target into an application.

        Args:
            target: User supplied application name.

        Returns:
            Registered Application.
        """

        application = (
            self._application_manager.find(
                target
            )
        )

        return OpenResult(
            kind="application",
            value=application,
        )