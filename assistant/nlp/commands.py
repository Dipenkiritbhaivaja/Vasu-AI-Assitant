"""
NLP command configuration.
"""

COMMAND_SYNONYMS = {
    "open": "open",
    "launch": "open",
    "start": "open",

    "close": "close",
    "terminate": "close",
    "kill": "close",

    "restart": "restart",
    "reboot": "restart",

    "find": "find",
    "locate": "find",
    "lookup": "find",

    "search": "search",
    "google": "search",

    "play": "play",

    "create": "create",
    "make": "create",
    "new": "create",
}

PRESERVE_PAYLOAD_COMMANDS = {
    "search",
    "play",
}