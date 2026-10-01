import logging

import httpx
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src import config
from src.chatbot.documents import process_document
from src.chatbot.services import ChatbotService
from src.chatbot.vectorstore import retrieve_chunks, store_embeddings


def configure_app() -> None:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        filename=config.LOG_FILE,
        format="%(asctime)s [%(levelname)s] %(message)s",
        force=True,
    )
    st.set_page_config(page_title="Local AI Chatbot", page_icon="🤖")


def render_history(chatbot: ChatbotService) -> None:
    for message in chatbot.history:
        if isinstance(message, HumanMessage):
            st.chat_message("user").write(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").write(message.content)


def process_uploaded_files(uploaded_files) -> None:
    if not uploaded_files:
        return

    st.write(f"Total files uploaded: {len(uploaded_files)}")
    for file in uploaded_files:
        st.write(f"📁 Processing: **{file.name}**")
        try:
            _, chunks, embeddings = process_document(file)
            store_embeddings(chunks, embeddings)
            st.success("Document processed successfully. You can now ask questions about it.")
        except ValueError as error:
            st.error(f"Error processing **{file.name}**: {error}")
        except UnicodeDecodeError:
            st.error(
                f"Could not read **{file.name}**. "
                "The file is not valid UTF-8 text."
            )


def main() -> None:
    configure_app()
    st.title("Local AI Chatbot")
    st.write("Welcome! Your Streamlit UI starts here.")

    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = ChatbotService()
    chatbot = st.session_state["chatbot"]

    user_input = st.chat_input("Enter your message", accept_file="multiple")
    text_message = user_input.text if user_input else ""
    context = ""

    if user_input:
        process_uploaded_files(user_input.files)
        if text_message:
            try:
                context = retrieve_chunks(text_message)
                st.write(f"User message: {text_message}")
                st.write(f"Retrieved {len(context)} relevant chunks from ChromaDB for context.")
                for index, chunk in enumerate(context, start=1):
                    st.write(f"Chunk {index}: {chunk}")
            except Exception:
                st.error("Could not retrieve document context.")

    render_history(chatbot)

    if user_input and text_message:
        try:
            response = chatbot.ask(text_message, context)
            st.chat_message("assistant").write(response)
            st.rerun()
        except httpx.ConnectError:
            st.error("Could not connect to Ollama. Please make sure Ollama is running.")
        except Exception:
            st.error("Something went wrong. Please try again.")


if __name__ == "__main__":
    main()
    