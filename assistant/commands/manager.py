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
from assistant.commands.handlers.open_command_handler import (
    OpenCommandHandler,
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
from assistant.files.manager import FileManager
from assistant.commands.handlers.find_file_handler import (
    FindFileHandler,
)
from assistant.commands.handlers.search_command_handler import (
    SearchCommandHandler,
)
from assistant.commands.handlers.play_command_handler import (
    PlayCommandHandler,
)
from assistant.system.service import (
    SystemService,
)
from assistant.commands.handlers.lock_command_handler import LockCommandHandler
from assistant.commands.handlers.shutdown_command_handler import (
    ShutdownCommandHandler,
)

from assistant.commands.handlers.rename_command_handler import (
    RenameCommandHandler,
)

from assistant.commands.handlers.delete_command_handler import (
    DeleteCommandHandler,
)

from assistant.commands.handlers.create_command_handler import (
    CreateCommandHandler,
)

from assistant.commands.handlers.copy_command_handler import (
    CopyCommandHandler,
)

from assistant.commands.handlers.move_command_handler import (
    MoveCommandHandler,
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
        file_manager: FileManager,
        system_service: SystemService,
    ) -> None: 

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )
        self._parser = CommandParser()
        self._application_manager = application_manager
        self._application_service = application_service
        self._browser_service = browser_service
        self._file_manager = file_manager
        self._system_service = system_service

        self._commands: dict[
            str,
            CommandInfo,
        ] = {
            "open": CommandInfo(
                handler=OpenCommandHandler(
                    self._application_manager,
                    self._application_service,
                    self._browser_service,
                    self._file_manager,
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
                handler=HelpCommandHandler(self,),
                usage="help",
                description="Show available commands.",
            ),
            "restart": CommandInfo(
                handler=RestartApplicationHandler(
                    self._application_manager,
                    self._application_service,
                    self._system_service,
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
            "status": CommandInfo(
                handler=StatusApplicationHandler(
                    self._application_manager,
                    self._application_service,
                ),
                usage="status <application>",
                description="Show whether an application is running.",
            ),
            "find": CommandInfo(
                handler=FindFileHandler(
                    self._file_manager,
                ),
                usage="find <file_name>",
                description="Search for files.",
            ),
            "search": CommandInfo(
                handler=SearchCommandHandler(
                    self._browser_service,
                ),
                usage="search <query>",
                description="Search Google.",
            ),
            "play": CommandInfo(
                handler=PlayCommandHandler(
                    self._browser_service,
                ),
                usage="play <query>",
                description="Play videos on YouTube.",
            ),
            "lock": CommandInfo(
                handler=LockCommandHandler(
                    self._system_service,
                ),
                usage="lock",
                description="Lock the computer.",
            ),
            "shutdown": CommandInfo(
                handler=ShutdownCommandHandler(
                    self._system_service,
                ),
                usage="shutdown",
                description="Shut down the computer.",
            ),
            "create": CommandInfo(
                handler=CreateCommandHandler(
                    self._file_manager,
                ),
                usage="create <file|folder> <name>",
                description="Create a new file or folder.",
            ),
            "delete": CommandInfo(
                handler=DeleteCommandHandler(
                    self._file_manager,
                ),
                usage="delete <file|folder> <name>",
                description="Delete a file or an empty folder.",
            ),
            "rename": CommandInfo(
                handler=RenameCommandHandler(
                    self._file_manager,
                ),
                usage="rename <file|folder> <old_name> to <new_name>",
                description="Rename a file or folder.",
            ),
            "copy": CommandInfo(
                handler=CopyCommandHandler(
                    self._file_manager,
                ),
                usage="copy <file|folder> <source> to <destination>",
                description="Copy a file or folder.",
            ),
            "move": CommandInfo(
                handler=MoveCommandHandler(
                    self._file_manager,
                ),
                usage="move <file|folder> <source> to <destination>",
                description="Move a file or folder.",
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