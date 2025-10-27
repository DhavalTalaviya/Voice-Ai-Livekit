"""Prompt template manager"""
import json
import logging
from pathlib import Path
from typing import Optional

from models.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages prompt templates"""

    def __init__(self, prompts_dir: str = "src/prompts/templates"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts: dict[str, PromptTemplate] = {}
        self._load_prompts()

    def _load_prompts(self):
        """Load all prompt templates from disk"""
        if not self.prompts_dir.exists():
            logger.warning(f"Prompts directory not found: {self.prompts_dir}")
            return

        for prompt_file in self.prompts_dir.glob("**/*.json"):
            try:
                with open(prompt_file, "r") as f:
                    data = json.load(f)
                    prompt = PromptTemplate(**data)
                    self.prompts[prompt.id] = prompt
                    logger.info(f"Loaded prompt: {prompt.id}")
            except Exception as e:
                logger.error(f"Failed to load prompt {prompt_file}: {e}")

    def get_prompt(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Get a prompt template by ID"""
        return self.prompts.get(prompt_id)

    def get_prompts_by_category(self, category: str) -> list[PromptTemplate]:
        """Get all prompts in a category"""
        return [p for p in self.prompts.values() if p.category == category]

    def get_organization_prompts(self, org_id: str) -> list[PromptTemplate]:
        """Get organization-specific prompts"""
        return [p for p in self.prompts.values() if p.organization_id == org_id]

    def reload(self):
        """Reload all prompts from disk"""
        self.prompts.clear()
        self._load_prompts()