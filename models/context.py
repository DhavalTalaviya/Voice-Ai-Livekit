"""Type-safe context models"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class UserContext(BaseModel):
    """User context information"""

    user_id: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    language: str = "en"
    timezone: str = "UTC"
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrganizationContext(BaseModel):
    """Organization-specific context"""

    org_id: str
    name: str
    industry: Optional[str] = None
    business_hours: Optional[dict[str, Any]] = None
    contact_info: dict[str, str] = Field(default_factory=dict)
    custom_settings: dict[str, Any] = Field(default_factory=dict)
    branding: dict[str, str] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    """Conversation state and history"""

    conversation_id: str
    user_id: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    messages: list[dict[str, Any]] = Field(default_factory=list)
    current_intent: Optional[str] = None
    variables: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentContext(BaseModel):
    """Complete agent context"""

    user: UserContext
    organization: OrganizationContext
    conversation: ConversationContext
    is_phone_call: bool = False
    call_metadata: dict[str, Any] = Field(default_factory=dict)

    def to_prompt_variables(self) -> dict[str, Any]:
        """Convert context to variables for prompt templates"""
        return {
            "user_name": self.user.name or "there",
            "org_name": self.organization.name,
            "org_industry": self.organization.industry or "general",
            "is_phone": self.is_phone_call,
            "language": self.user.language,
            "current_time": datetime.utcnow().isoformat(),
            **self.conversation.variables,
        }