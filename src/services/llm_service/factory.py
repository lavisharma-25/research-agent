from src.core.settings import settings

from src.services.llm_service.gemini import GeminiService
from src.services.llm_service.nvidia import NvidiaService
from src.services.llm_service.openai import OpenAIService
from src.services.llm_service.claude import ClaudeService


class LLMFactory:

    PROVIDERS = {
        "gemini": GeminiService,
        "nvidia": NvidiaService,
        "openai": OpenAIService,
        "claude": ClaudeService,
    }

    @classmethod
    def create_llm(cls):

        provider = settings.LLM_PROVIDER.lower()

        service = cls.PROVIDERS.get(provider)

        if not service:
            raise ValueError(
                f"Unsupported provider: {provider}"
            )

        return service.create_llm(
            settings.LLM_MODEL
        )

llm = LLMFactory.create_llm()