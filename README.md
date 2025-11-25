# WordApp

A personal vocabulary building application designed to help manage and learn new words. This project was developed for personal use to streamline the process of capturing and reviewing new vocabulary.

**Developed using [Antigravity](https://github.com/google-deepmind/antigravity)** (Agentic AI Coding Assistant).

## Features

- **macOS Native App**: A clean, native macOS interface built with SwiftUI.
- **Notion Integration**: Automatically saves defined words to a Notion database for easy review and tracking.
- **AI-Powered Definitions**: Uses LLMs (Large Language Models) to provide accurate definitions and examples.
- **English Word Extraction**: Automatically detects and extracts English words from user input, correcting typos and filtering invalid prompts.
- **Search History**: Keeps a session-based history of searched words.
- **Dockerized Backend**: The backend is containerized for consistent deployment and easy setup.

## Tech Stack

- **Frontend**: Swift (SwiftUI)
- **Backend**: Python (FastAPI)
- **Database**: Notion (via API)
- **AI**: LangChain, OpenAI GPT
- **Deployment**: Docker

## Getting Started

### Prerequisites

- Docker
- Xcode (for macOS app)
- Notion Integration Token & Database ID
- OpenAI API Key

### Backend Setup

1. Clone the repository.
2. Create a `.env` file in `backend/` with your API keys:
    ```env
    OPENAI_API_KEY=your_key
    NOTION_TOKEN=your_token
    NOTION_DATABASE_ID=your_db_id
    LANGSMITH_API_KEY=your_langsmith_key (optional)
    ```
3. Run with Docker:
    ```bash
    docker-compose up --build
    ```

### Frontend Setup

1. Open `WordApp/WordApp.xcodeproj` in Xcode.
2. Build and run the application.
