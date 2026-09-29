import logging

import httpx
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src import config
from src.chatbot.services import ChatbotService

logging.basicConfig(
    level=config.LOG_LEVEL,
    filename=config.LOG_FILE,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖"
)

st.title("Local AI Chatbot")
st.write("Welcome! Your Streamlit UI starts here.")

if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = ChatbotService()

chatbot = st.session_state["chatbot"]

user_input = st.chat_input("Enter your message")

for message in chatbot.history:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

if user_input:
    try:
        chatbot.ask(user_input)
        st.rerun()

    except httpx.ConnectError:
        st.error("Could not connect to Ollama. Please make sure Ollama is running.")

    except Exception:
        st.error("Something went wrong. Please try again.")
    