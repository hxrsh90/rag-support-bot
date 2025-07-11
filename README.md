# RAG Support Bot

A Retrieval-Augmented Generation (RAG) support bot using LangChain, FAISS, HuggingFace, and Ollama.

## Features
- Document ingestion and chunking
- Embedding with sentence-transformers/all-MiniLM-L6-v2
- Vector search with FAISS
- LLM-powered answers via Ollama (Gemma2:2b)
- Flask API for question answering

## Customizing Context

You can add your own `.txt` files to the `rag_api/support_docs/` directory to provide custom context for any use case, industry, or knowledge base. For example, you can add:
- Company FAQs
- Product manuals
- Policies and procedures
- Knowledge base articles

After adding or updating files, **rebuild the FAISS index**:
```sh
python build_index.py
```
This will update the context your bot uses to answer questions.

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
   python app.py
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

## n8n Integration

You can easily use this bot in an n8n workflow to automate question answering. Here’s how:

1. **Open n8n** (self-hosted or cloud).
2. **Create a new workflow.**
3. **Paste the following JSON into the workflow import dialog:**

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "url": "http://localhost:5000/ask",
        "options": {},
        "bodyParametersUi": {
          "parameter": [
            {
              "name": "query",
              "value": "What is your return policy?"
            }
          ]
        },
        "headerParametersUi": {
          "parameter": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        }
      },
      "id": 1,
      "name": "Ask RAG Bot",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ],
  "connections": {}
}
```

4. **Edit the `query` value** to ask any question you want.
5. **Run the workflow**. The response from the bot will be available in the output of the HTTP Request node.

> **Tip:** You can connect this node to other n8n nodes (like Telegram, Slack, or Email) to automate support answers.

## Security
- No private keys or sensitive files are included.
- `.gitignore` excludes secrets, venvs, and temp files.

## License
MIT 