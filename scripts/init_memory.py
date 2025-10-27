"""Initialize memory database"""
import asyncio
import sys
from pathlib import Path

# Add main directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from memory.storage import MemoryStorage

async def main():
    """Initialize the memory database"""
    print("🗄️  Initializing memory database...")

    storage = MemoryStorage()
    await storage.initialize()

    print("Memory database initialized successfully!")
    print(f"   Location: {storage.db_path}")


if __name__ == "__main__":
    asyncio.run(main())