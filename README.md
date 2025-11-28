# Local Context Engine

A privacy-focused, local RAG (Retrieval-Augmented Generation) application that allows you to chat with your PDF documents using **Llama 3.2** and **Ollama**.

## Features

*   **100% Local**: No data leaves your machine.
*   **Fast Inference**: Uses the optimized Llama 3.2 SLM.
*   **Modern UI**: Built with Streamlit, featuring a dark mode, glassmorphism design, and responsive feedback mechanisms.
*   **Feedback Loop**: Built-in 👍/👎 system to log hallucinations and improve performance.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: You must have Ollama installed and running.
    *   [Download Ollama](https://ollama.com/)
    *   Pull the model: `ollama pull llama3.2`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd "Local Context Engine"
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install streamlit langchain langchain-community chromadb
    ```

## Usage

1.  **Start the application**:
    ```bash
    streamlit run app.py
    ```

2.  **Upload Documents**:
    *   Open the sidebar.
    *   Drag and drop your PDF files.
    *   Click **Process Documents**.

3.  **Chat**:
    *   Ask questions about your documents in the chat input.
    *   View the latency metrics for each response.
    *   Use the 👍/👎 buttons to provide feedback (logged to `logs.json`).

## Project Structure

*   `app.py`: Main Streamlit application and UI logic.
*   `rag_engine.py`: Core RAG logic (loading, splitting, embedding, retrieving).
*   `logs.json`: Stores user feedback and performance metrics.
*   `SHIP_REPORT.md`: Detailed analysis of the build process and model performance.
