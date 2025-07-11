import os
from flask import Flask, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Flask app
app = Flask(__name__)

# Load Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS vector store
index_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'rag_index'))
db = FAISS.load_local(
    folder_path=index_dir,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Use Gemma from Ollama
llm = Ollama(model="qwen3:1.7b")

# Build RAG pipeline
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=True
)

import traceback

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        print("🔍 Received data:", data)

        query = data.get("query", "")
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Get RAG response
        result = qa.invoke(query)
        print("🧠 RAG result:", result)

        raw_answer = result["result"]

        # Clean model reasoning output
        think_content = ""
        answer = raw_answer.strip()

        if "<think>" in raw_answer and "</think>" in raw_answer:
            import re
            match = re.search(r"<think>(.*?)</think>", raw_answer, re.DOTALL)
            if match:
                think_content = match.group(1).strip()
            answer = raw_answer.split("</think>")[-1].strip()

        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]

        print("🧼 Final Answer:", answer)
        print("📚 Sources:", sources)
        if think_content:
            print("🧠 Model Reasoning:\n", think_content)

        return jsonify({
            "query": query,
            "answer": answer,
            "reasoning": think_content,
            "sources": sources
        })

    except Exception as e:
        print("❌ ERROR:", e)
        import traceback
        traceback.print_exc()  # 🧠 this shows full stack trace
        return jsonify({"error": str(e)}), 500


       


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
