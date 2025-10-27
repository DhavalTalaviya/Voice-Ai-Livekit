"""Test memory system"""
import pytest
from memory.conversation_memory import ConversationMemory
from memory.storage import MemoryStorage
from models.context import UserContext


@pytest.mark.asyncio
async def test_conversation_creation():
    """Test creating a conversation"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    user = UserContext(user_id="user123", name="John")
    conversation = await memory.create_conversation(user)

    assert conversation.user_id == user.user_id
    assert conversation.conversation_id is not None
    
    await storage.close()


@pytest.mark.asyncio
async def test_message_logging():
    """Test logging messages"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    user = UserContext(user_id="user123", name="John")
    conversation = await memory.create_conversation(user)

    # Add messages
    await memory.add_message(conversation.conversation_id, "user", "Hello")
    await memory.add_message(conversation.conversation_id, "assistant", "Hi there!")

    # Get history
    history = await memory.get_conversation_history(conversation.conversation_id)

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there!"
    
    await storage.close()


@pytest.mark.asyncio
async def test_user_profile():
    """Test user profile storage"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    # Save profile
    await memory.update_user_profile(
        "user123", {"name": "John Doe", "email": "john@example.com"}
    )

    # Get context
    context = await memory.get_user_context("user123")

    assert context is not None
    assert context["profile"]["name"] == "John Doe"
    assert context["profile"]["email"] == "john@example.com"
    
    await storage.close()


@pytest.mark.asyncio
async def test_conversation_history_limit():
    """Test conversation history with limit"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    user = UserContext(user_id="user123")
    conversation = await memory.create_conversation(user)

    # Add multiple messages
    for i in range(10):
        await memory.add_message(
            conversation.conversation_id, "user", f"Message {i}"
        )

    # Get limited history
    history = await memory.get_conversation_history(
        conversation.conversation_id, limit=5
    )

    assert len(history) == 5
    
    await storage.close()


@pytest.mark.asyncio
async def test_multiple_conversations():
    """Test multiple conversations for same user"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    user = UserContext(user_id="user123")

    # Create multiple conversations
    conv1 = await memory.create_conversation(user, metadata={"channel": "web"})
    conv2 = await memory.create_conversation(user, metadata={"channel": "phone"})

    # Add messages to each
    await memory.add_message(conv1.conversation_id, "user", "Hello from web")
    await memory.add_message(conv2.conversation_id, "user", "Hello from phone")

    # Get user's conversations
    context = await memory.get_user_context(user.user_id)

    assert context is not None
    assert context["total_conversations"] == 2
    
    await storage.close()


@pytest.mark.asyncio
async def test_conversation_summary():
    """Test conversation summary generation"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    memory = ConversationMemory(storage)
    
    user = UserContext(user_id="user123")
    conversation = await memory.create_conversation(user)

    # Add some messages
    await memory.add_message(conversation.conversation_id, "user", "Hello")
    await memory.add_message(conversation.conversation_id, "assistant", "Hi there!")
    await memory.add_message(conversation.conversation_id, "user", "How are you?")

    # Get summary
    summary = await memory.get_conversation_summary(conversation.conversation_id)

    assert "3 messages" in summary
    
    await storage.close()