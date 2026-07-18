"""
Database Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from assistant.database.base import BaseDatabase

from assistant.core.logger import LoggerManager

class DatabaseManager(BaseDatabase):
    """
    Handles SQLite database operations.
    """

    def __init__(self, database_path: str) -> None:
        self.logger = LoggerManager.get_logger(self.__class__.__name__)

        self.database_path = Path(database_path)

        self.connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        """
        Open a connection to the SQLite database.
        """

        if self.connection is not None:
            return

        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(self.database_path)

            self.connection.row_factory = sqlite3.Row

            self._initialize_database()

            self.logger.info("Database connected successfully.")

        except sqlite3.Error:
            self.logger.exception("Failed to connect to the database.")
            raise

    def close(self) -> None:
        """
        Close the database connection.
        """

        if self.connection is None:
            return

        self.connection.close()
        self.connection = None

        self.logger.info("Database connection closed.")

    def execute(
            self,
            query: str,
            parameters: tuple[object, ...] = (),
        ) -> sqlite3.Cursor:
        """
        Execute an SQL query.
        """

        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()

            cursor.execute(query, parameters)

            self.connection.commit()

            return cursor

        except sqlite3.Error:
            self.logger.exception(
                "Failed to execute SQL query."
            )
            raise

    def fetch_one(
        self,
        query: str,
        parameters: tuple[object, ...] = (),
    ) -> sqlite3.Cursor :
        """
        Return one row.
        """

        cursor = self.execute(query, parameters)

        return cursor.fetchone()
    
    def fetch_all(
        self,
        query: str,
        parameters: tuple[object, ...] = (),
    ) -> sqlite3.Cursor :
        """
        Return all rows.
        """

        cursor = self.execute(query, parameters)

        return cursor.fetchall()
    
    def _initialize_database(self) -> None:
        """
        Create all required tables.

        This method is called once after a successful
        database connection.
        """
        self._create_memories_table()
    
    def _create_memories_table(self) -> None:
        """
        Create the memories table if it does not already exist.
        """

        query = """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
        """

        self.execute(query)

        self.logger.info("Verified 'memories' table exists.")