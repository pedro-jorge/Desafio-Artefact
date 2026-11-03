from pathlib import Path

from langchain_groq import ChatGroq

from src.config import settings

class LLMClient:
    def __init__(self):
        self.client = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY.get_secret_value(),
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
        )


    def ask(self, question: str, sources: str) -> str:
        system_prompt = settings.PROMPT.format(question=question, sources=sources)
        response = self.client.invoke(system_prompt)
        return response.content