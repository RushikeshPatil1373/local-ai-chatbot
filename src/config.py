"""Application configuration values."""
import os
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")
SYSTEM_PROMPT = "You are a helpful AI assistant. Give concise and clear answers. Explain technical concepts in beginner-friendly language. Avoid using jargon or complex terminology unless necessary, and provide examples when possible. If you don't know the answer, it's okay to say so."

LOG_LEVEL = "INFO"
LOG_FILE = "chatbot.log"
