# Local AI Chatbot

## Overview

Local AI Chatbot is a Python application that connects a Streamlit chat interface to a locally hosted Ollama model through LangChain. The application keeps a bounded in-memory conversation history for the current Streamlit session and writes application logs to `chatbot.log`.

## Features

### Currently implemented

- Local model responses through Ollama and `ChatOllama`
- LangChain prompt template with a fixed system prompt
- Streamlit chat interface with text input
- Multiple file upload in the chat input
- UTF-8 text extraction for uploaded files
- In-memory conversation history using LangChain `HumanMessage` and `AIMessage` objects
- History trimming to the five most recent exchanges
- Specific error message for Ollama connection failures
- Logging for successful responses, history trimming, connection errors, and unexpected errors
- Model selection through the `MODEL_NAME` environment variable

Uploaded file contents are currently displayed in the interface only; they are not added to the model prompt or conversation history.

## Project Structure

```text
local-ai-chatbot/
├── app.py                         # Streamlit entry point and UI
├── requirements.txt               # Currently listed Python 
├── README.md
├── .gitignore
├── python                         # Empty tracked file
├── .env                           # Local configuration; ignored by 
├── chatbot.log                    # Runtime log; ignored by Git
├── src/
│   ├── __init__.py
│   ├── config.py                  # Environment loading and app 
│   └── chatbot/
│       ├── __init__.py
│       ├── documents.py            # UTF-8 uploaded-file extraction
│       ├── services.py             # Ollama/LangChain service and 
│       └── test.py                 # Interactive console chatbot 
└── tests/
     └── .gitkeep                   # No automated tests currently present
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

    The current `requirements.txt` lists `streamlit`, `python-dotenv`, and `ollama`. The source code also imports `httpx`, `langchain-core`, and `langchain-ollama`, so install those packages if they are not already available in the environment:

    ```bash
    pip install httpx langchain-core langchain-ollama
    ```

4. Install and start Ollama, then download a model:

    ```bash
    ollama pull qwen2.5:1.5b
    ollama list
    ```

## Configuration

Create a `.env` file in the project root:

```env
MODEL_NAME=qwen2.5:1.5b
```

`src/config.py` loads this value with `python-dotenv`. If `MODEL_NAME` is not set, the application defaults to `qwen2.5:1.5b`. The system prompt, log level (`INFO`), and log filename (`chatbot.log`) are defined as constants in `src/config.py`, not loaded from `.env`.

Do not commit `.env`. It is excluded by `.gitignore`.

## Running the Application

Start the Streamlit application from the project root:

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit. Enter a message to send it to the configured Ollama model. You can also attach files; the current implementation extracts and displays their UTF-8 text without sending that text to the model.

## How It Works

1. `app.py` configures logging and initializes one `ChatbotService` in `st.session_state`.
2. `ChatbotService` creates a LangChain `ChatPromptTemplate` containing the system prompt, prior messages, and the new user input.
3. The prompt is passed to `ChatOllama` using the configured model name.
4. The user prompt and model response are appended to the service history and the response is displayed in Streamlit.
5. The UI catches Ollama connection errors separately from other unexpected errors.

## Conversation History

History is stored in memory on the `ChatbotService` instance for the active Streamlit session. Each completed exchange adds one `HumanMessage` and one `AIMessage`. After each response, `trim_history()` keeps at most ten messages, representing the five most recent exchanges. There is no database or persistent history storage, and uploaded file text is not included in the history.

## Development

The application code is organized into the Streamlit entry point, configuration, chatbot service, and document extraction modules. `src/chatbot/test.py` can be run as an interactive terminal chatbot and exits when the user enters `exit`.

There are currently no automated tests in `tests/`; that directory contains only `.gitkeep`. Runtime logs, virtual environments, environment files, Python caches, and common IDE files are excluded by `.gitignore`.

## Future Improvements

- Add automated unit and integration tests
- Add the missing runtime dependencies to `requirements.txt`
- Send extracted document text to the model with clear file and prompt boundaries
- Support additional document formats and extraction errors
- Add persistent conversation storage or configurable history management
- Improve the chat UI and deployment workflow

## License

No license file or license declaration is currently included in the repository.
