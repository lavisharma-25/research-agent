from abc import ABC, abstractmethod


class BaseLLMService(ABC):

    @classmethod
    @abstractmethod
    def create_llm(cls, model_name: str):
        pass