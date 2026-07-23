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
from assistant.commands.handlers.status_handler import (
    StatusApplicationHandler,
)
from assistant.browser.service import BrowserService
from assistant.files.service import FileService
from assistant.files.manager import FileManager
from assistant.commands.handlers.find_file_handler import (
    FindFileHandler,
)
from assistant.commands.command_key import (
    CommandKey,
)


class CommandManager:
    """
    Coordinates command parsing and execution.
    """

    def __init__(
        self,
        application_manager: ApplicationManager,
        application_service: ApplicationService,
        browser_service: BrowserService,
    ) -> None: 

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )
        self._parser = CommandParser()
        self._application_manager = application_manager
        self._application_service = application_service
        self._browser_service = browser_service
        self._file_service = FileService()
        self._file_manager = FileManager(
            self._file_service,
        )

        self._commands: dict[
            CommandKey,
            CommandInfo,
        ] = {
            CommandKey(
                "open",
                "application",
            ): CommandInfo(
                handler=OpenApplicationHandler(
                    self._application_manager,
                    self._application_service,
                    self._browser_service,
                ),
                usage="open application <application>",
                description="Open a registered application.",
            ),
            CommandKey(
                "close",
                "application",
            ): CommandInfo(
                handler=CloseApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="close application <application>",
                description="Close a running application.",
            ),
            "help": CommandInfo(
                handler=HelpCommandHandler(),
                usage="help",
                description="Show available commands.",
            ),
            CommandKey(
                "restart",
                "application",
            ): CommandInfo(
                handler=RestartApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="restart application <application>",
                description="Restart a registered application.",
            ),
            CommandKey(
                "list",
                "applications",
            ): CommandInfo(
                handler=ListApplicationsHandler(
                    self._application_manager,
                ),
                usage="list applications",
                description="List all registered applications.",
            ),
            CommandKey(
                "status",
                "applications",
            ): CommandInfo(
                handler=StatusApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="status application <application>",
                description="Show whether an application is running.",
            ),
            CommandKey(
                "find",
                "file",
            ): CommandInfo(
                handler=FindFileHandler(
                    self._file_manager,
                ),
                usage="find <file_name>",
                description="Search for files.",
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

        command_key = CommandKey(
            action=command.action,
            resource=command.resource,
        )

        command_info = self._commands.get(
            command_key
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
    ) -> dict[CommandKey, CommandInfo]:
        """
        Return all registered commands.
        """

        return self._commands