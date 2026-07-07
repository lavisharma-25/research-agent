from langchain_openai import ChatOpenAI

from src.core.settings import settings
from src.services.llm_service.base import BaseLLMService


class OpenAIService(BaseLLMService):

    @classmethod
    def create_llm(cls, model_name: str):

        return ChatOpenAI(
            api_key=settings.NVIDIA_API_KEY,
            base_url="https://integrate.api.nvidia.com/v1",
            model="moonshotai/kimi-k2.6",
        )