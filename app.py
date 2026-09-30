import logging

import httpx
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src import config
from src.chatbot.services import ChatbotService
from src.chatbot.documents import extract_text

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

user_input = st.chat_input(
    "Enter your message",
    accept_file="multiple"
)

if user_input:
    # 1. Get the text message
    text_message = user_input.text

    if text_message:
        st.write(f"User message: {text_message}")

    # 2. Get uploaded files
    uploaded_files = user_input.files

    if uploaded_files:
        st.write(f"Total files uploaded: {len(uploaded_files)}")

        for file in uploaded_files:
            st.write(f"📁 Processing: **{file.name}**")
            try:
                extracted_text = extract_text(file)
                st.write("### Extracted text")
                st.write(extracted_text)
            except UnicodeDecodeError:
                st.error(
                    f"Could not read **{file.name}**. "
                    "The file is not valid UTF-8 text."
                )

for message in chatbot.history:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

if user_input:
    try:
        if text_message:
            response = chatbot.ask(text_message)
            st.chat_message("assistant").write(response)
            st.rerun()

    except httpx.ConnectError:
        st.error("Could not connect to Ollama. Please make sure Ollama is running.")

    except Exception:
        st.error("Something went wrong. Please try again.")
    