"""
Exceptions for the File module.
"""


class FileSearchError(Exception):
    """
    Base exception for file operations.
    """


class FileNotFoundError(FileSearchError):
    """
    Raised when a file cannot be found.
    """