# Local AI Chatbot

## Overview

Local AI Chatbot is a Streamlit application that connects to locally hosted Ollama models through LangChain. It accepts UTF-8 text files, creates embeddings, stores them in ChromaDB, and retrieves relevant document chunks for chat context. Conversation history is kept in memory for the current Streamlit session, and application logs are written to `chatbot.log`.

## Features

### Currently implemented

- Local model responses through Ollama and `ChatOllama`
- LangChain prompt template with a fixed system prompt
- Streamlit chat interface with text input
- Multiple file upload in the chat input
- UTF-8 text extraction for uploaded files
- Recursive document chunking with configurable chunk size
- Ollama embeddings for uploaded document chunks
- Persistent ChromaDB storage and similarity retrieval
- Retrieved document context included in chat prompts
- In-memory conversation history using LangChain `HumanMessage` and `AIMessage` objects
- History trimming to the five most recent exchanges
- Specific error message for Ollama connection failures
- Logging for successful responses, history trimming, connection errors, and unexpected errors
- Chat model selection through the `MODEL_NAME` environment variable
- Embedding model selection through the `EMBEDDING_MODEL_NAME` environment variable

## Project Structure

```text
local-ai-chatbot/
├── app.py                         # Streamlit entry point and UI
├── requirements.txt               # Pinned runtime and test dependencies
├── pytest.ini                     # Pytest import path and warning configuration
├── README.md
├── .gitignore
├── .env                           # Local configuration; ignored by Git
├── chatbot.log                    # Runtime log; ignored by Git
├── chroma_db/                      # Persistent vector database; ignored by Git
├── src/
│   ├── __init__.py
│   ├── config.py                  # Environment loading and app constants
│   └── chatbot/
│       ├── __init__.py
│       ├── documents.py            # Extraction, chunking, and embeddings
│       ├── services.py             # Ollama/LangChain chat service
│       ├── vectorstore.py          # ChromaDB storage and retrieval
│       └── test.py                 # Interactive console chatbot
└── tests/
    ├── test_app.py                # Streamlit startup smoke test
    ├── test_documents.py          # Document unit tests
    ├── test_services.py           # Chat service unit tests
    └── test_vectorstore.py        # Vector store unit tests
```

`venv/` may also exist locally as a virtual environment, but it is ignored by Git and is not part of the project source.

## Prerequisites

- Python 3.10 or newer
- Git
- [Ollama](https://ollama.com/) installed and running
- An Ollama model available locally, such as `qwen2.5:1.5b`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/RushikeshPatil1373/local-ai-chatbot.git
    cd local-ai-chatbot
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    ```

    Windows PowerShell:

    ```powershell
    venv\Scripts\Activate.ps1
    ```

    Windows Command Prompt:

    ```cmd
    venv\Scripts\activate.bat
    ```

3. Install the dependencies listed in the repository:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Install and start Ollama, then download both a chat model and an embedding model:

    ```bash
    ollama pull qwen2.5:1.5b
    ollama pull nomic-embed-text
    ollama list
    ```

## Configuration

Create a `.env` file in the project root:

```env
MODEL_NAME=qwen2.5:1.5b
EMBEDDING_MODEL_NAME=nomic-embed-text
```

`src/config.py` loads these values with `python-dotenv`. If they are not set, the application defaults to `qwen2.5:1.5b` for chat and `nomic-embed-text` for embeddings. The system prompt, log level (`INFO`), log filename (`chatbot.log`), and ChromaDB path (`./chroma_db`) are defined as constants in `src/config.py`.

Do not commit `.env`. It is excluded by `.gitignore`.

## Running the Application

Start the Streamlit application from the project root:

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit. Upload one or more UTF-8 text files to index them, then enter a message. The application retrieves the most relevant stored chunks and sends them as context to the configured Ollama chat model.

## Running Tests

Run the complete local test suite from the project root:

```bash
pytest -q
```

The tests mock Ollama and ChromaDB network/database operations, so they do not require a running Ollama server. The Streamlit test verifies that the application starts successfully.

## How It Works

1. `app.py` configures logging and initializes one `ChatbotService` in `st.session_state`.
2. Uploaded files are decoded as UTF-8, split into chunks, embedded with `OllamaEmbeddings`, and stored in ChromaDB.
3. A user question is embedded and used to retrieve relevant chunks from ChromaDB.
4. `ChatbotService` creates a LangChain `ChatPromptTemplate` containing the system prompt, prior messages, retrieved context, and new user input.
5. The prompt is passed to `ChatOllama`, and the exchange is appended to the bounded session history.
6. The UI reports document, retrieval, Ollama connection, and unexpected runtime errors without exposing stack traces.

## Conversation History

History is stored in memory on the `ChatbotService` instance for the active Streamlit session. Each completed exchange adds one `HumanMessage` and one `AIMessage`. After each response, `trim_history()` keeps at most ten messages, representing the five most recent exchanges. There is no database or persistent history storage, and uploaded file text is not included in the history.

## Development

The application code is organized into the Streamlit entry point, configuration, chat service, document processing, and vector store modules. `src/chatbot/test.py` can be run as an interactive terminal chatbot and exits when the user enters `exit`. Runtime logs, virtual environments, environment files, ChromaDB data, Python caches, and common IDE files are excluded by `.gitignore`.

## Future Improvements

- Send extracted document text to the model with clear file and prompt boundaries
- Support additional document formats and extraction errors
- Add persistent conversation storage or configurable history management
- Improve the chat UI and deployment workflow

## License

No license file or license declaration is currently included in the repository.
