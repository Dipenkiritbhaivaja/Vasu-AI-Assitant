from abc import ABC, abstractmethod
from typing import Any


class BaseDatabase(ABC):
    """
    Abstract base class defining the contract for all
    database implementations.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple[Any, ...] = ()) -> None:
        """Execute a query that does not return rows."""
        pass

    @abstractmethod
    def fetch_one(
        self,
        query: str,
        params: tuple[Any, ...] = ()
    ) -> tuple[Any, ...] | None:
        """Return a single row."""
        pass

    @abstractmethod
    def fetch_all(
        self,
        query: str,
        params: tuple[Any, ...] = ()
    ) -> list[tuple[Any, ...]]:
        """Return multiple rows."""
        pass
