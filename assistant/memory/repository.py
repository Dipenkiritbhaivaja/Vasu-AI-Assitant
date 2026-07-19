from __future__ import annotations

from assistant.database.base import BaseDatabase
from assistant.memory.models import MemoryRecord
from datetime import datetime

class MemoryRepository:
    """
    Handles persistence operations for memories.

    This class is responsible only for interacting with the
    database. It contains no business logic.
    """

    def __init__(self, database: BaseDatabase) -> None:
        self._database = database

    def add(self, memory: MemoryRecord) -> int:
        """
        Store a new memory and return its database ID.
        """

        cursor = self._database.execute(
            """
            INSERT INTO memories (
                title,
                content,
                category,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                memory.title,
                memory.content,
                memory.category,
                memory.created_at.isoformat(),
                memory.updated_at.isoformat(),
            ),
        )

        return cursor.lastrowid

    def get_by_id(
        self,
        memory_id: int,
    ) -> MemoryRecord | None:
        """
        Retrieve a memory by its ID.
        """

        row = self._database.fetch_one(
            """
            SELECT *
            FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        if row is None:
            return None

        return MemoryRecord.from_row(row)

    def get_all(self) -> list[MemoryRecord]:
        """
        Return all stored memories.
        """

        rows = self._database.fetch_all(
            """
            SELECT *
            FROM memories
            ORDER BY id ASC
            """
        )

        return [
            MemoryRecord.from_row(row)
            for row in rows
        ]

    def update(
        self,
        memory: MemoryRecord,
    ) -> bool:
        """
        Update an existing memory.

        Returns:
            True if a row was updated.
            False if the memory does not exist.
        """

        if memory.id is None:
            raise ValueError(
                "Cannot update a memory without an ID."
            )

        cursor = self._database.execute(
            """
            UPDATE memories
            SET
                title = ?,
                content = ?,
                category = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                memory.title,
                memory.content,
                memory.category,
                memory.updated_at.isoformat(),
                memory.id,
            ),
        )

        return cursor.rowcount > 0

    def delete(
        self,
        memory_id: int,
    ) -> bool:
        """
        Delete a memory by its ID.

        Returns:
            True if a memory was deleted.
            False if no matching memory exists.
        """

        cursor = self._database.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        return cursor.rowcount > 0