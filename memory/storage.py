"""Persistent storage for conversation memory"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import aiosqlite

logger = logging.getLogger(__name__)


class MemoryStorage:
    """SQLite-based storage for conversation memory"""

    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._connection = None  # Keep connection alive for :memory:
        
        # Create directory for file-based DB
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    async def _get_connection(self):
        """Get or create database connection"""
        if self.db_path == ":memory:":
            # For in-memory DB, reuse the same connection
            if self._connection is None:
                self._connection = await aiosqlite.connect(self.db_path)
            return self._connection
        else:
            # For file-based DB, create new connection each time
            return await aiosqlite.connect(self.db_path)

    async def initialize(self):
        """Initialize database tables"""
        conn = await self._get_connection()
        
        # Conversations table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                metadata TEXT
            )
            """
        )

        # Messages table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
            """
        )

        # User profiles table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                phone_number TEXT,
                email TEXT,
                preferences TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        await conn.commit()
        
        # Verify tables were created
        async with conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ) as cursor:
            tables = await cursor.fetchall()
            logger.info(f"Created tables: {[t[0] for t in tables]}")
        
        # Close connection if not in-memory
        if self.db_path != ":memory:":
            await conn.close()

    async def save_conversation(
        self, conversation_id: str, user_id: str, metadata: Optional[dict[str, Any]] = None
    ):
        """Save or update a conversation"""
        conn = await self._get_connection()
        
        await conn.execute(
            """
            INSERT OR REPLACE INTO conversations
            (conversation_id, user_id, start_time, metadata)
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                user_id,
                datetime.utcnow().isoformat(),
                json.dumps(metadata or {}),
            ),
        )
        await conn.commit()
        
        if self.db_path != ":memory:":
            await conn.close()

    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """Save a message to conversation history"""
        conn = await self._get_connection()
        
        await conn.execute(
            """
            INSERT INTO messages
            (conversation_id, role, content, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
                datetime.utcnow().isoformat(),
                json.dumps(metadata or {}),
            ),
        )
        await conn.commit()
        
        if self.db_path != ":memory:":
            await conn.close()

    async def get_conversation_history(
        self, conversation_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """
        Get conversation message history
        Returns messages in chronological order (oldest first)
        """
        conn = await self._get_connection()
        conn.row_factory = aiosqlite.Row
        
        # Get messages ordered by timestamp ascending (oldest first)
        async with conn.execute(
            """
            SELECT role, content, timestamp, metadata
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
            """,
            (conversation_id, limit),
        ) as cursor:
            rows = await cursor.fetchall()
            result = [
                {
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                }
                for row in rows
            ]
        
        if self.db_path != ":memory:":
            await conn.close()
        
        return result

    async def get_user_conversations(
        self, user_id: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Get user's recent conversations"""
        conn = await self._get_connection()
        conn.row_factory = aiosqlite.Row
        
        async with conn.execute(
            """
            SELECT conversation_id, start_time, end_time, metadata
            FROM conversations
            WHERE user_id = ?
            ORDER BY start_time DESC
            LIMIT ?
            """,
            (user_id, limit),
        ) as cursor:
            rows = await cursor.fetchall()
            result = [
                {
                    "conversation_id": row["conversation_id"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                }
                for row in rows
            ]
        
        if self.db_path != ":memory:":
            await conn.close()
        
        return result

    async def save_user_profile(self, user_id: str, profile: dict[str, Any]):
        """Save or update user profile"""
        conn = await self._get_connection()
        now = datetime.utcnow().isoformat()
        
        # Check if profile exists
        async with conn.execute(
            "SELECT user_id FROM user_profiles WHERE user_id = ?", (user_id,)
        ) as cursor:
            existing = await cursor.fetchone()
        
        if existing:
            # Update existing profile
            await conn.execute(
                """
                UPDATE user_profiles
                SET name = ?, phone_number = ?, email = ?, preferences = ?, updated_at = ?
                WHERE user_id = ?
                """,
                (
                    profile.get("name"),
                    profile.get("phone_number"),
                    profile.get("email"),
                    json.dumps(profile.get("preferences", {})),
                    now,
                    user_id,
                ),
            )
        else:
            # Insert new profile
            await conn.execute(
                """
                INSERT INTO user_profiles
                (user_id, name, phone_number, email, preferences, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    profile.get("name"),
                    profile.get("phone_number"),
                    profile.get("email"),
                    json.dumps(profile.get("preferences", {})),
                    now,
                    now,
                ),
            )
        
        await conn.commit()
        
        if self.db_path != ":memory:":
            await conn.close()

    async def get_user_profile(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get user profile"""
        conn = await self._get_connection()
        conn.row_factory = aiosqlite.Row
        
        async with conn.execute(
            "SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            result = None
            if row:
                result = {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "phone_number": row["phone_number"],
                    "email": row["email"],
                    "preferences": json.loads(row["preferences"])
                    if row["preferences"]
                    else {},
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
        
        if self.db_path != ":memory:":
            await conn.close()
        
        return result

    async def verify_tables(self) -> dict[str, bool]:
        """Verify all required tables exist"""
        conn = await self._get_connection()
        
        tables = {}
        for table_name in ["conversations", "messages", "user_profiles"]:
            async with conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            ) as cursor:
                result = await cursor.fetchone()
                tables[table_name] = result is not None
        
        if self.db_path != ":memory:":
            await conn.close()
        
        return tables

    async def close(self):
        """Close the database connection"""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None