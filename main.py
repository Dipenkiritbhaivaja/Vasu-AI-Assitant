from assistant.applications.manager import (
    ApplicationManager,
)
from assistant.commands.manager import (
    CommandManager,
)

application_manager = ApplicationManager(
    "data/applications.json"
)

command_manager = CommandManager(
    application_manager,
)

command_manager.execute("open notepad")