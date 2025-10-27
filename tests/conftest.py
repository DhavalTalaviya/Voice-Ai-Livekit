"""Pytest configuration and shared fixtures"""
import pytest
from models.context import UserContext


@pytest.fixture
def sample_user():
    """Create a sample user context"""
    return UserContext(
        user_id="test_user_123",
        name="Test User",
        email="test@example.com"
    )