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
index_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rag_index'))
db = FAISS.load_local(
    folder_path=index_dir,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Use Gemma from Ollama
llm = Ollama(model="gemma2:2b")

# Build RAG pipeline
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=True
)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        result = qa(query)
        answer = result["result"]
        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]

        return jsonify({
            "query": query,
            "answer": answer,
            "sources": sources
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 