from typing import Any
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether


class LLMProvider(ABC):
    model: Any
    model_name: str

    @abstractmethod
    def invoke(self, query):
        pass

    @abstractmethod
    async def ainvoke(self, prompt):
        pass


class LMStudioProvider(LLMProvider):
    def invoke(self, query):
        return self.model.invoke(query)

    def __new__(cls, host: str, model_name: str, temperature: float = 0):
        return ChatOpenAI(api_key="...", model=model_name, base_url=host, temperature=temperature)

    async def ainvoke(self, query):
        return self.model.ainvoke(query)


class TogetherProvider(LLMProvider):
    def invoke(self, query):
        return self.model.invoke(query)

    def __new__(cls, model_name: str, temperature: float = 0):
        return ChatTogether(model=model_name, temperature=temperature)

    async def ainvoke(self, query):
        return self.model.ainvoke(query)
