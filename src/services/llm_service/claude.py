from langchain_anthropic import ChatAnthropic

from src.core.settings import settings
from src.services.llm_service.base import BaseLLMService


class ClaudeService(BaseLLMService):

    def __init__(self, api_key: str):
        self.model = ChatAnthropic(
            model=settings.CLAUDE_MODEL,
            api_key=api_key,
        )

    def invoke(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content