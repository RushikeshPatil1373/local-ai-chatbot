# Local AI Chatbot

A local-first AI chatbot built with Python, LangChain, Ollama, and Streamlit. The chatbot runs locally on your machine and supports conversation history, configurable models, error handling, logging, and bounded chat history.

## Overview

This project is a local AI chatbot designed to run with a locally hosted Ollama model. LangChain is used to connect the chatbot logic with the model, while Streamlit provides the web-based user interface.

### Current Features

* Local LLM inference using Ollama
* LangChain-based chatbot service
* Configurable model through `.env`
* System prompt configuration
* Conversation history using LangChain message objects
* Bounded conversation history to prevent unlimited history growth
* Streamlit chat interface
* Error handling for Ollama connection failures
* Application logging
* Git/GitHub project structure

## Conversation History

The chatbot maintains conversation history inside `ChatbotService` using LangChain message objects.

Each exchange contains:

* `HumanMessage` for the user's input
* `AIMessage` for the model's response

The application limits stored history to a fixed number of recent exchanges so that the conversation context does not grow indefinitely.

## Project Structure

```text
local-ai-chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env                 # Local configuration; not committed to Git
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── chatbot/
│       ├── __init__.py
│       └──  services.py
└── tests/
    └── .gitkeep
```

> `.env` is listed here to explain the local configuration file. It is ignored by Git and should not be committed to the repository.

## Prerequisites

* Python 3.10 or newer
* Git
* Ollama
* A local Ollama model

The project was developed and tested with Python 3.14.5 and Ollama.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/RushikeshPatil1373/local-ai-chatbot.git
cd local-ai-chatbot
```

### 2. Create and activate a virtual environment

Create the virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Install and start Ollama

Install Ollama and make sure the Ollama service is running.

Then pull the model used by the project:

```bash
ollama pull qwen2.5:1.5b
```

You can verify that the model is available with:

```bash
ollama list
```

### 6. Configure the model

Create a `.env` file in the project root:

```env
MODEL_NAME=qwen2.5:1.5b
```

The application reads the model name from the environment configuration.

> Do not commit `.env` to Git because it is included in `.gitignore`.

### 7. Run the chatbot

From the project root:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can open the chatbot in your browser.

## Git Ignore

The project uses `.gitignore` to prevent local and generated files from being committed.

Important ignored files and directories include:

* `venv/`
* `.env`
* `*.log`
* Python cache files
* IDE configuration files

## Development

The chatbot logic is separated from the Streamlit UI through `ChatbotService`.

The main responsibilities are:

* `app.py` — Streamlit user interface
* `src/chatbot/services.py` — chatbot/model interaction and conversation history
* `src/config.py` — application configuration
* `.env` — local environment-specific configuration

## Future Improvements

### Implemented Decisions

* Conversation history is bounded using a last-N exchanges strategy (chosen over token-based trimming or summarization for simplicity at this stage)

### Still Open

* Automated unit and integration tests
* Token-based history management or summarization (if last-N proves insufficient later)
* Better UI features
* Deployment of the application
* Additional local model support
## License

This project is currently for learning and development purposes. A license can be added when the project is ready for distribution.
