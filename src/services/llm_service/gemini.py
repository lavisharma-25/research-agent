from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

from src.core.settings import settings
from src.services.llm_service.base import BaseLLMService


class GeminiService(BaseLLMService):

    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
        HarmBlockThreshold.BLOCK_NONE
    }

    @classmethod
    def create_llm(cls, model_name: str):

        if settings.GEMINI_PROVIDER.lower() == "vertex":

            return ChatGoogleGenerativeAI(
                model=model_name,
                project=settings.credentials.project_id,
                credentials=settings.credentials,
                location=settings.LOCATION,
                vertexai=True,
                temperature=0,
                safety_settings=cls.safety_settings,
                model_kwargs={
                    "thinking": 0,
                },
            )

        elif settings.GEMINI_PROVIDER.lower() == "api_key":

            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0,
                safety_settings=cls.safety_settings,
                model_kwargs={
                    "thinking": 0,
                },
            )

        raise ValueError(
            f"Unsupported GEMINI_PROVIDER: {settings.GEMINI_PROVIDER}"
        )