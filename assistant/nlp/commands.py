"""
NLP command configuration.
"""

COMMAND_SYNONYMS = {
    # Open
    "open": "open",
    "launch": "open",
    "start": "open",

    # Close
    "close": "close",
    "terminate": "close",
    "kill": "close",

    # Restart
    "restart": "restart",
    "reboot": "restart",

    # Find
    "find": "find",
    "locate": "find",
    "lookup": "find",

    # Search
    "search": "search",
    "google": "search",

    # Play
    "play": "play",

    # Create
    "create": "create",
    "make": "create",
    "new": "create",

    # Delete
    "delete": "delete",

    # Rename
    "rename": "rename",

    # Help
    "help": "help",

    # List
    "list": "list",

    # Status
    "status": "status",

    # Lock
    "lock": "lock",

    # Shutdown
    "shutdown": "shutdown",
}

PRESERVE_PAYLOAD_COMMANDS = {
    "search",
    "play",
}