"""View conversation memory"""
import asyncio
import sys
from pathlib import Path

# Add main directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.storage import MemoryStorage


async def view_conversations(user_id: str = None):
    """View conversations from memory"""
    storage = MemoryStorage()
    await storage.initialize()

    if user_id:
        print(f"\nConversations for user: {user_id}")
        conversations = await storage.get_user_conversations(user_id)

        for conv in conversations:
            print(f"\n  Conversation: {conv['conversation_id']}")
            print(f"  Started: {conv['start_time']}")
            print(f"  Metadata: {conv['metadata']}")

            # Get messages
            messages = await storage.get_conversation_history(conv["conversation_id"])
            print(f"  Messages: {len(messages)}")

            for msg in messages[:5]:  # Show first 5 messages
                print(f"    [{msg['role']}] {msg['content'][:100]}...")
    else:
        print("\nAll conversations")
        # You'd need to add a method to list all conversations
        print("   Use: python scripts/view_memory.py <user_id>")


if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(view_conversations(user_id))