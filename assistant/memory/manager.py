"""
Memory Manager for VASU AI ASSISTANT.
"""


from __future__ import annotations

from datetime import datetime

from assistant.memory.models import MemoryRecord
from assistant.memory.repository import MemoryRepository
from assistant.core.logger import LoggerManager
from assistant.memory.exceptions import (
    MemoryValidationError,
)

class MemoryManager:
    """
    Handles memory-related business logic.
    """

    def __init__(self, repository: MemoryRepository) -> None:
        self._repository = repository

        self.logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

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

        self._validate_memory_data(
            title,
            content,
            category,
        )

        now = datetime.now()

        memory = MemoryRecord(
            id=None,
            title=title.strip(),
            content=content.strip(),
            category=category.strip(),
            created_at=now,
            updated_at=now,
        )

        memory_id = self._repository.add(memory)

        self.logger.info(
            "Added memory ID %s ('%s').",
            memory_id,
            memory.title,
        )

        return memory_id
    
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
    
    def update_memory(
        self,
        memory: MemoryRecord,
    ) -> bool:
        """
        Update an existing memory.
        """

        if memory.id is None:
            raise MemoryValidationError(
                "Memory must have an ID."
            )
        
        self._validate_memory_data(
            memory.title,
            memory.content,
            memory.category,
        )

        memory.updated_at = datetime.now()

        success = self._repository.update(memory)

        if success:
            self.logger.info(
                "Updated memory ID %s.",
                memory.id,
            )

        return success
    
    def delete_memory(
        self,
        memory_id: int,
    ) -> bool:
        """
        Delete a memory by its ID.
        """

        success = self._repository.delete(memory_id)

        if success:
            self.logger.info(
                "Deleted memory ID %s.",
                memory_id,
            )

        return success
    
    def _validate_memory_data(
        self,
        title: str,
        content: str,
        category: str,
    ) -> None:
        """
        Validate memory fields before storing them.
        """

        if not title.strip():
            raise MemoryValidationError(
                "Memory title cannot be empty."
            )

        if not content.strip():
            raise MemoryValidationError(
                "Memory content cannot be empty."
            )

        if not category.strip():
            raise MemoryValidationError(
                "Memory category cannot be empty."
            )