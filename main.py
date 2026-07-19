from assistant.database.manager import DatabaseManager
from assistant.memory.manager import MemoryManager
from assistant.memory.repository import MemoryRepository
from assistant.memory.exceptions import MemoryValidationError

database = DatabaseManager("data/vasu.db")
database.connect()

repository = MemoryRepository(database)
manager = MemoryManager(repository)

try:
    manager.add_memory(
        title="   ",
        content="Some content",
        category="Test",
    )
except MemoryValidationError as error:
    print("Validation Error:", error)

database.close()