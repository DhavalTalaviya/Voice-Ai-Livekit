"""Conversation memory manager"""
import logging
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from models.context import ConversationContext, UserContext
from memory.storage import MemoryStorage

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manages conversation memory and context"""

    def __init__(self, storage: MemoryStorage):
        self.storage = storage

    async def create_conversation(
        self, user: UserContext, metadata: Optional[dict[str, Any]] = None
    ) -> ConversationContext:
        """Create a new conversation"""
        conversation_id = str(uuid4())

        await self.storage.save_conversation(conversation_id, user.user_id, metadata)

        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=user.user_id,
            metadata=metadata or {},
        )

        logger.info(f"Created conversation {conversation_id} for user {user.user_id}")
        return context

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """Add a message to conversation history"""
        await self.storage.save_message(conversation_id, role, content, metadata)
        logger.debug(f"Added {role} message to conversation {conversation_id}")

    async def get_conversation_history(
        self, conversation_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get conversation message history"""
        return await self.storage.get_conversation_history(conversation_id, limit)

    async def get_conversation_summary(self, conversation_id: str) -> str:
        """Generate a summary of the conversation"""
        history = await self.get_conversation_history(conversation_id, limit=20)

        if not history:
            return "No conversation history."

        # Simple summary - in production, use LLM to generate
        message_count = len(history)
        user_messages = sum(1 for msg in history if msg["role"] == "user")
        assistant_messages = sum(1 for msg in history if msg["role"] == "assistant")

        return (
            f"Conversation has {message_count} messages "
            f"({user_messages} from user, {assistant_messages} from assistant)."
        )

    async def get_user_context(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get user context including profile and recent conversations"""
        profile = await self.storage.get_user_profile(user_id)
        conversations = await self.storage.get_user_conversations(user_id, limit=5)

        if not profile and not conversations:
            return None

        return {
            "profile": profile,
            "recent_conversations": conversations,
            "total_conversations": len(conversations),
        }

    async def update_user_profile(self, user_id: str, profile_data: dict[str, Any]):
        """Update user profile"""
        await self.storage.save_user_profile(user_id, profile_data)
        logger.info(f"Updated profile for user {user_id}")