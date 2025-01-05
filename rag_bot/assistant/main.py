from dotenv import load_dotenv
load_dotenv()

from .prompt import SYSTEM_PROMPT
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from rag_bot.groq.chat import chat_groq

def _get_llm(platform: str, model: str, temperature: float):
    llm = {
        "groq": chat_groq,
    }
    return llm[platform](model, temperature)


class ChatBot():

    def __init__(self, platform: str, model: str, temperature: float):
        
        self.llm = _get_llm(platform, model, temperature)
        self.prompt_tokens = 0
        self.completion_tokens = 0


    def stream_response(self, documents: str, chat_messages: list):
        """
        Yields response chunks from the LLM model.    
        """
        messages = [("system", SYSTEM_PROMPT)]
        messages.extend(chat_messages)
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm | StrOutputParser()
        response = chain.stream({"documents": documents})
        for chunk in response:
            yield chunk