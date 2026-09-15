from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .. import config
class ChatbotService:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.model = OllamaLLM(model=self.model_name)
        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", config.SYSTEM_PROMPT),
            ("human", "{input}")
        ])

    def ask(self, prompt:str)-> str:
        prompt = self.chat_prompt_template.format_prompt(input=prompt).to_string()

        return  self.model.invoke(prompt)