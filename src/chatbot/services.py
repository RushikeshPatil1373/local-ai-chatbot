import httpx
import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from .. import config

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.model = ChatOllama(model=self.model_name)
        self.history = []
        self.chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", config.SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                ("system", "Context: {context}"),
                ("human", "{input}"),
            ]
        )
        self.chain = self.chat_prompt_template | self.model

    def trim_history(self, max_exchanges: int = 5):
        if max_exchanges < 0:
            raise ValueError("max_exchanges cannot be negative.")

        max_messages = max_exchanges * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]
            logger.info(f"Trimmed history to the last {max_exchanges} exchanges.")

    def ask(self, prompt: str, context: str = "") -> str:
        try:
            response = self.chain.invoke(
                {
                    "history": self.history,
                    "context": context,
                    "input": prompt,
                }
            )
            self.history.append(HumanMessage(content=prompt))
            self.history.append(AIMessage(content=response.content))
            self.trim_history()
            logger.info("Chatbot responded successfully")
            return response.content
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise