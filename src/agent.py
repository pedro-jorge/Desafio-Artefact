from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from src.tools import (
    get_document,
    consult_sql,
    get_schema
)
from src.config import settings

class Agent:
    def __init__(self):
        self.agent = create_agent(
            model=ChatOllama(
                model=settings.LLM_MODEL,
                base_url=settings.LLM_BASE_URL,
                temperature=settings.LLM_TEMPERATURE,
                num_ctx=settings.NUM_CTX_TOKENS,
            ),
            tools=[consult_sql],
            system_prompt=settings.PROMPT.replace("{schema}", get_schema()).replace("{document}", get_document()),
        )
        
        print(settings.PROMPT.replace("{schema}", get_schema()).replace("{document}", get_document()))

    def ask(self, question: str) -> str:
        return self.agent.invoke({
            "messages": [{
                "role": "user",
                "content": question
            }]
        })