"""Test prompt system"""
import pytest
from datetime import datetime

from models.context import AgentContext, ConversationContext, OrganizationContext, UserContext
from models.prompts import PromptTemplate, PromptVariable, PromptVariableType
from prompts.renderer import PromptRenderer


def test_prompt_rendering():
    """Test prompt template rendering"""
    template = PromptTemplate(
        id="test",
        name="Test",
        description="Test template",
        template="Hello {{ user_name }} from {{ org_name }}!",
        variables=[
            PromptVariable(
                name="user_name", type=PromptVariableType.STRING, description="Name", required=True
            ),
            PromptVariable(
                name="org_name", type=PromptVariableType.STRING, description="Org", required=True
            ),
        ],
        category="test",
        version="1.0.0",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

    user = UserContext(user_id="u1", name="John")
    org = OrganizationContext(org_id="o1", name="TechCorp")
    conv = ConversationContext(conversation_id="c1", user_id="u1")

    context = AgentContext(user=user, organization=org, conversation=conv)

    renderer = PromptRenderer()
    result = renderer.render(template, context)

    assert "Hello John from TechCorp!" == result


def test_missing_required_variable():
    """Test that missing required variables raise error"""
    template = PromptTemplate(
        id="test",
        name="Test",
        description="Test",
        template="Hello {{ missing }}",
        variables=[
            PromptVariable(
                name="missing", type=PromptVariableType.STRING, description="M", required=True
            )
        ],
        category="test",
        version="1.0.0",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

    user = UserContext(user_id="u1")
    org = OrganizationContext(org_id="o1", name="Corp")
    conv = ConversationContext(conversation_id="c1", user_id="u1")

    context = AgentContext(user=user, organization=org, conversation=conv)

    renderer = PromptRenderer()

    with pytest.raises(ValueError):
        renderer.render(template, context)