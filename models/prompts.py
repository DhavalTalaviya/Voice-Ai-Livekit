"""Prompt template models"""
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class PromptVariableType(str, Enum):
    """Types of prompt variables"""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"


class PromptVariable(BaseModel):
    """A variable used in prompts"""

    name: str
    type: PromptVariableType
    description: str
    default: Optional[Any] = None
    required: bool = False


class PromptTemplate(BaseModel):
    """A prompt template with metadata"""

    id: str
    name: str
    description: str
    template: str
    variables: list[PromptVariable] = Field(default_factory=list)
    category: str = "general"
    version: str = "1.0.0"
    organization_id: Optional[str] = None
    created_at: str
    updated_at: str
    tags: list[str] = Field(default_factory=list)

    def get_required_variables(self) -> list[str]:
        """Get list of required variable names"""
        return [var.name for var in self.variables if var.required]

    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate that context has all required variables"""
        required = set(self.get_required_variables())
        provided = set(context.keys())
        return required.issubset(provided)