from typing import Any, List

import requests

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult

from src.core.settings import settings
from src.services.llm_service.base import BaseLLMService


class NvidiaChatModel(BaseChatModel):
    api_key: str
    model: str
    max_tokens: int = 16384
    temperature: float = 1.0
    top_p: float = 1.0

    @property
    def _llm_type(self) -> str:
        return "nvidia_chat"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: List[str] | None = None,
        run_manager: Any = None,
        **kwargs,
    ) -> ChatResult:

        payload_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"

            elif isinstance(msg, AIMessage):
                role = "assistant"

            elif isinstance(msg, SystemMessage):
                role = "system"

            else:
                role = "user"

            payload_messages.append(
                {
                    "role": role,
                    "content": msg.content,
                }
            )

        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            },
            json={
                "model": self.model,
                "messages": payload_messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()

        content = (
            result["choices"][0]["message"]["content"]
            .strip()
        )

        message = AIMessage(content=content)

        generation = ChatGeneration(
            message=message
        )

        return ChatResult(
            generations=[generation]
        )


class NvidiaService(BaseLLMService):

    @classmethod
    def create_llm(cls, model_name: str):

        return NvidiaChatModel(
            api_key=settings.NVIDIA_API_KEY,
            model=model_name,
        )