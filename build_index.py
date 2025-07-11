from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

# Load all text files from the support_docs directory
loader = DirectoryLoader("rag_api/support_docs", glob="**/*.txt")
documents = loader.load()

# Split docs into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Check for empty chunks
if not chunks:
    raise ValueError("No document chunks found. Please check your document directory and files.")

# Load a secure embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build FAISS index and save it using LangChain's save_local
index_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rag_index'))
db = FAISS.from_documents(chunks, embedding_model)
db.save_local(index_dir)

print("✅ FAISS index built and saved in rag_index/") 