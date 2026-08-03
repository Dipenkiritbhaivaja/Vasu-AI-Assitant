"""
Custom exceptions for the Command module.
"""


class CommandError(Exception):
    """Base exception for command-related errors."""

class CommandParseError(CommandError):
    """Raised when a command cannot be parsed."""

class CommandHandlerError(CommandError):
    """
    Raised when no handler exists
    for a command.
    """

class InvalidCommandUsageError(Exception):
    """
    Raised when the user provides an invalid
    command or missing arguments.
    """