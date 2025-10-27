"""Test type-safe models"""
import pytest
from datetime import datetime

from models.context import AgentContext, ConversationContext, OrganizationContext, UserContext
from models.prompts import PromptTemplate, PromptVariable, PromptVariableType


def test_user_context():
    """Test user context creation"""
    user = UserContext(
        user_id="user123",
        name="John Doe",
        phone_number="+1234567890",
        email="john@example.com",
    )

    assert user.user_id == "user123"
    assert user.name == "John Doe"
    assert user.language == "en"


def test_organization_context():
    """Test organization context"""
    org = OrganizationContext(
        org_id="org123",
        name="Tech Corp",
        industry="technology",
    )

    assert org.org_id == "org123"
    assert org.name == "Tech Corp"


def test_agent_context_to_variables():
    """Test converting agent context to prompt variables"""
    user = UserContext(user_id="user123", name="John")
    org = OrganizationContext(org_id="org123", name="Tech Corp", industry="tech")
    conv = ConversationContext(conversation_id="conv123", user_id="user123")

    agent_context = AgentContext(
        user=user,
        organization=org,
        conversation=conv,
        is_phone_call=True,
    )

    variables = agent_context.to_prompt_variables()

    assert variables["user_name"] == "John"
    assert variables["org_name"] == "Tech Corp"
    assert variables["org_industry"] == "tech"
    assert variables["is_phone"] is True


def test_prompt_template_validation():
    """Test prompt template variable validation"""
    template = PromptTemplate(
        id="test",
        name="Test",
        description="Test template",
        template="Hello {{ name }}",
        variables=[
            PromptVariable(
                name="name",
                type=PromptVariableType.STRING,
                description="User name",
                required=True,
            )
        ],
        category="test",
        version="1.0.0",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

    # Valid context
    assert template.validate_context({"name": "John"}) is True

    # Invalid context (missing required)
    assert template.validate_context({}) is False