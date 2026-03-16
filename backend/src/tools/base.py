"""Tool base class -- simple data fetchers for future use."""

from abc import ABC, abstractmethod


class Tool(ABC):
    """Base class for tools that fetch or compute data for the agent."""

    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs: object) -> dict:
        """Execute the tool and return results."""
        ...
