"""Sub-agent base class -- independent reasoning agents for future use."""

from abc import ABC, abstractmethod

from ..tools.base import Tool


class SubAgent(ABC):
    """Base class for sub-agents that perform independent reasoning tasks."""

    name: str
    description: str
    system_prompt: str
    tools: list[Tool]

    @abstractmethod
    def run(self, question: str, context: dict) -> str:
        """Run the sub-agent with a question and context."""
        ...
