from abc import ABC, abstractmethod

from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse


class LLMProvider(ABC):
    """
    Common interface for every LLM provider.

    Providers receive the complete agent conversation so they can
    reason over previous messages and tool results.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        """
        Generate the next response using the conversation history.
        """
        raise NotImplementedError