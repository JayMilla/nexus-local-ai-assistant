# NEXUS

NEXUS is a locally hosted AI assistant built with Python and Ollama.

The project uses a locally running Qwen3 4B language model to provide conversational AI without relying on a cloud API.

## Features

- Local AI inference
- Interactive terminal chat
- Conversation history
- Custom system prompt
- Streaming responses
- Error handling
- Modular Python architecture

## Architecture

User
 │
 ▼
main.py
 │
 ├── Conversation Manager
 │
 └── Ollama Client
          │
          ▼
    Ollama API
          │
          ▼
       Qwen3 4B

## Project Structure

nexus/
│
├── main.py
├── config.py
├── conversation.py
├── ollama_client.py
├── requirements.txt
├── README.md
└── .gitignore

## Requirements
- Python 3.12+
- Ollama
- Qwen3 4B

## Setup

Clone the repository:
Bash:
    git clone <repository-url>
    cd nexus

Create a virtual environment:
Bash:
    python -m venv .venv

Activate the virtual environment on Windows PowerShell:
PowerShell: 
    .venv\Scripts\Activate.ps1

Install dependencies:
PowerShell:
    pip install -r requirements.txt

Install the Qwen3 4B model:
PowerShell:
    ollama pull qwen3:4b

Run the application: 
PowerShell:
    python main.py

## Current Limitations

- Conversation history is lost when the application closes.
- The interface currently runs in the terminal.
- The assistant cannot yet interact with external applications or hardware.

## Future Plans

- Persistent memory using SQLite
- Voice input and output
- Tool use
- Local document search
- Hardware integration
- Desktop interface
