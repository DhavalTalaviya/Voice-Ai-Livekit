"""Prompt template renderer"""
import logging
from typing import Any

from jinja2 import Environment, Template, TemplateError

from models.context import AgentContext
from models.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class PromptRenderer:
    """Renders prompt templates with context"""

    def __init__(self):
        self.env = Environment(autoescape=True)

    def render(self, prompt: PromptTemplate, context: AgentContext) -> str:
        """
        Render a prompt template with agent context

        Args:
            prompt: The prompt template to render
            context: The agent context

        Returns:
            Rendered prompt string

        Raises:
            ValueError: If required variables are missing
            TemplateError: If template rendering fails
        """
        # Convert context to variables
        variables = context.to_prompt_variables()

        # Validate required variables
        if not prompt.validate_context(variables):
            missing = set(prompt.get_required_variables()) - set(variables.keys())
            raise ValueError(f"Missing required variables: {missing}")

        # Render template
        try:
            template = self.env.from_string(prompt.template)
            rendered = template.render(**variables)
            logger.debug(f"Rendered prompt {prompt.id}")
            return rendered
        except TemplateError as e:
            logger.error(f"Failed to render prompt {prompt.id}: {e}")
            raise

    def render_string(self, template_string: str, variables: dict[str, Any]) -> str:
        """Render a template string directly"""
        try:
            template = self.env.from_string(template_string)
            return template.render(**variables)
        except TemplateError as e:
            logger.error(f"Failed to render template: {e}")
            raise