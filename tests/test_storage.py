"""Test storage layer"""
import pytest
from memory.storage import MemoryStorage


@pytest.mark.asyncio
async def test_storage_initialization():
    """Test that storage initializes correctly"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # Verify tables exist
    tables = await storage.verify_tables()
    
    assert tables["conversations"] is True, "conversations table not created"
    assert tables["messages"] is True, "messages table not created"
    assert tables["user_profiles"] is True, "user_profiles table not created"
    
    await storage.close()


@pytest.mark.asyncio
async def test_save_and_retrieve_conversation():
    """Test saving and retrieving conversation"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # Save a conversation
    await storage.save_conversation("conv123", "user456", {"test": "data"})
    
    # Retrieve it
    conversations = await storage.get_user_conversations("user456")
    
    assert len(conversations) == 1
    assert conversations[0]["conversation_id"] == "conv123"
    
    await storage.close()


@pytest.mark.asyncio
async def test_save_and_retrieve_message():
    """Test saving and retrieving messages"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # First create a conversation
    await storage.save_conversation("conv123", "user456")
    
    # Save messages
    await storage.save_message("conv123", "user", "Hello")
    await storage.save_message("conv123", "assistant", "Hi there!")
    
    # Retrieve messages
    messages = await storage.get_conversation_history("conv123")
    
    # Debug: print what we got
    print(f"\nMessages: {messages}")
    for i, msg in enumerate(messages):
        print(f"  {i}: {msg['role']} - {msg['content']}")
    
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Hi there!"
    
    await storage.close()


@pytest.mark.asyncio
async def test_save_and_retrieve_user_profile():
    """Test saving and retrieving user profile"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # Save profile
    await storage.save_user_profile("user123", {
        "name": "John Doe",
        "email": "john@example.com",
        "phone_number": "+1234567890"
    })
    
    # Retrieve profile
    profile = await storage.get_user_profile("user123")
    
    assert profile is not None
    assert profile["name"] == "John Doe"
    assert profile["email"] == "john@example.com"
    assert profile["phone_number"] == "+1234567890"
    
    await storage.close()


@pytest.mark.asyncio
async def test_update_user_profile():
    """Test updating existing user profile"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # Save profile
    await storage.save_user_profile("user123", {
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    # Update profile
    await storage.save_user_profile("user123", {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone_number": "+9876543210"
    })
    
    # Retrieve updated profile
    profile = await storage.get_user_profile("user123")
    
    assert profile["name"] == "Jane Doe"
    assert profile["email"] == "jane@example.com"
    assert profile["phone_number"] == "+9876543210"
    
    await storage.close()


@pytest.mark.asyncio
async def test_multiple_conversations():
    """Test multiple conversations for same user"""
    storage = MemoryStorage(db_path=":memory:")
    await storage.initialize()
    
    # Create multiple conversations
    await storage.save_conversation("conv1", "user123", {"channel": "web"})
    await storage.save_conversation("conv2", "user123", {"channel": "phone"})
    
    # Get user's conversations
    conversations = await storage.get_user_conversations("user123")
    
    assert len(conversations) == 2
    
    await storage.close()