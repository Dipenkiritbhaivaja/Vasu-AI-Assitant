from dataclasses import dataclass
from datetime import datetime
import sqlite3

@dataclass(slots=True)
class MemoryRecord:
    """
    Represents a single memory stored by the assistant.
    """

    id: int | None
    title: str
    content: str
    category: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "MemoryRecord":
        """
        Create a MemoryRecord from a SQLite row.
        """

        return cls(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            category=row["category"],
            created_at=(
                datetime.fromisoformat(row["created_at"])
                if row["created_at"] is not None
                else None
            ),
            updated_at=(
                datetime.fromisoformat(row["updated_at"])
                if row["updated_at"] is not None
                else None
            ),
        )