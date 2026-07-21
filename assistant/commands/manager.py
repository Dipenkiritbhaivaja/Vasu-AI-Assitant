"""
Command Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.applications.service import (
    ApplicationService,
)
from assistant.commands.exceptions import (
    CommandHandlerError,
)
from assistant.commands.handlers.base import (
    BaseCommandHandler,
)
from assistant.commands.handlers.open_handler import (
    OpenApplicationHandler,
)
from assistant.commands.parser import (
    CommandParser,
)
from assistant.core.logger import (
    LoggerManager,
)
from assistant.commands.handlers.close_handler import (
    CloseApplicationHandler,
)
from assistant.commands.handlers.help_handler import (
    HelpCommandHandler,
)
from assistant.commands.command_info import (
    CommandInfo,
)
from assistant.commands.handlers.restart_handler import (
    RestartApplicationHandler,
)
from assistant.commands.handlers.list_applications_handler import (
    ListApplicationsHandler,
)


class CommandManager:
    """
    Coordinates command parsing and execution.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

        self._parser = CommandParser()

        self._application_manager = application_manager
        self._application_service = application_service

        self._commands: dict[
            str,
            CommandInfo,
        ] = {
            "open": CommandInfo(
                handler=OpenApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="open <application>",
                description="Open a registered application.",
            ),
            "close": CommandInfo(
                handler=CloseApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="close <application>",
                description="Close a running application.",
            ),
            "help": CommandInfo(
                handler=HelpCommandHandler(),
                usage="help",
                description="Show available commands.",
            ),
            "restart": CommandInfo(
                handler=RestartApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="restart <application>",
                description="Restart a registered application.",
            ),
            "list": CommandInfo(
                handler=ListApplicationsHandler(
                    self._application_manager,
                ),
                usage="list applications",
                description="List all registered applications.",
            ),
        }

    def execute(
        self,
        text: str,
    ) -> None:
        """
        Parse and execute a command.
        """

        command = self._parser.parse(text)

        command_info = self._commands.get(
            command.action
        )

        if command_info is None:
            raise CommandHandlerError(
                f"Unknown command: '{command.action}'."
            )

        self._logger.info(
            "Executing command '%s'.",
            command.action,
        )

        command_info.handler.execute(command)

    def get_registered_commands(
        self,
    ) -> dict[str, CommandInfo]:
        """
        Return all registered commands.
        """

        return self._commands