"""
Custom exceptions for the Memory module.
"""


class MemoryError(Exception):
    """
    Base exception for all memory-related errors.
    """


class MemoryValidationError(MemoryError):
    """
    Raised when memory data is invalid.
    """


class MemoryNotFoundError(MemoryError):
    """
    Raised when a requested memory does not exist.
    """