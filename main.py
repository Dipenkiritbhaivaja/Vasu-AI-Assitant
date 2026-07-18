from assistant.database.manager import DatabaseManager
from assistant.memory.manager import MemoryManager
from assistant.memory.repository import MemoryRepository

database = DatabaseManager("data/vasu.db")
database.connect()

repository = MemoryRepository(database)
manager = MemoryManager(repository)

manager.add_memory(
    title="Manager API Test",
    content="Testing manager methods.",
    category="Test",
)

print()

print("Single memory")
print("-" * 30)

memory = manager.get_memory(1)

print(memory)

print()

print("All memories")
print("-" * 30)

for memory in manager.get_all_memories():
    print(memory)

database.close()