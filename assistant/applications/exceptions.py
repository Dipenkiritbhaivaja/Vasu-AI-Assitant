"""
Custom exceptions for the Application module.
"""


class ApplicationError(Exception):
    """
    Base exception for application-related errors.
    """


class ApplicationNotFoundError(ApplicationError):
    """
    Raised when an application is not registered.
    """