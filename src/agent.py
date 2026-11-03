from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import (
    get_document,
    consult_sql,
)
from config import settings

class Agent:
    def __init__(self):
        self.agent = create_agent(
            model=ChatGroq(
                groq_api_key=settings.GROQ_API_KEY.get_secret_value(),
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
            ),
            tools=[get_document],
            system_prompt=settings.PROMPT,
        )

    def ask(self, question: str) -> str:
        return self.agent.invoke({
            "messages": [{
                "role": "user",
                "content": question
            }]
        })
