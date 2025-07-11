# RAG Support Bot

A Retrieval-Augmented Generation (RAG) support bot using LangChain, FAISS, HuggingFace, and Ollama.

## Features
- Document ingestion and chunking
- Embedding with sentence-transformers/all-MiniLM-L6-v2
- Vector search with FAISS
- LLM-powered answers via Ollama (Gemma2:2b)
- Flask API for question answering

## Setup

1. **Clone the repo:**
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Build the FAISS index:**
   ```sh
   python build_index.py
   ```
4. **Start Ollama and pull the model:**
   ```sh
   ollama pull gemma2:2b
   ollama serve
   ```
5. **Run the Flask app:**
   ```sh
   python rag_api/support_docs/app.py
   ```
6. **Ask questions:**
   Send a POST request to `http://localhost:5000/ask` with JSON `{ "query": "Your question" }`

## Docker

1. **Build the image:**
   ```sh
   docker build -t rag-support-bot .
   ```
2. **Run the container:**
   ```sh
   docker run -p 5000:5000 rag-support-bot
   ```

> **Note:** Ollama must be running and accessible from the container. For local testing, run Ollama on the host and use `--network=host` (Linux) or set up port forwarding (Windows/Mac).

## Security
- No private keys or sensitive files are included.
- `.gitignore` excludes secrets, venvs, and temp files.

## License
MIT 