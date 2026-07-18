"""
Memory Manager for VASU AI ASSISTANT.
"""

from __future__ import annotations

from datetime import datetime

from assistant.memory.models import MemoryRecord
from assistant.memory.repository import MemoryRepository


class MemoryManager:
    """
    Handles memory-related business logic.
    """

    def __init__(self, repository: MemoryRepository) -> None:
        self._repository = repository

    def add_memory(
        self,
        title: str,
        content: str,
        category: str,
    ) -> int:
        """
        Create and store a new memory.

        Returns:
            int: Database ID of the newly created memory.
        """

        now = datetime.now()

        memory = MemoryRecord(
            id=None,
            title=title.strip(),
            content=content.strip(),
            category=category.strip(),
            created_at=now,
            updated_at=now,
        )

        return self._repository.add(memory)
    
    def get_memory(
        self,
        memory_id: int,
    ) -> MemoryRecord | None:
        """
        Return a memory by its ID.
        """

        return self._repository.get_by_id(memory_id)
    
    def get_all_memories(
        self,
    ) -> list[MemoryRecord]:
        """
        Return all stored memories.
        """

        return self._repository.get_all()