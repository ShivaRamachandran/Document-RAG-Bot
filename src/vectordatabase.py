from huggingface_hub import login
import os
import time
import torch
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download

# Disable SSL verification for Hugging Face
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
os.environ["CURL_CA_BUNDLE"] = ""

# Load environment variables from .env file
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Login to Hugging Face with SSL verification disabled
login(token=HUGGINGFACEHUB_API_TOKEN)

# Disable SSL verification globally in requests
requests.packages.urllib3.disable_warnings()
requests.Session().verify = False

# Directory where files are stored
DIRECTORY_PATH = "./data"

# Load documents from directory
def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            print(f"Skipping unsupported file: {filename}")
            continue
        
        documents.extend(loader.load())

    return documents

# Chunk documents into smaller parts
def chunk_documents(documents, chunk_size=1000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
    return text_splitter.split_documents(documents)

# Load embedding model from Hugging Face Hub with SSL disabled
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Download model files (optional, for offline access)
hf_hub_download(repo_id=MODEL_NAME, filename="config.json")

# Load tokenizer and model (disable SSL verification)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)

# Function to generate embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().tolist()  # CLS token representation

# Initialize Pinecone with SSL disabled
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "rag"

# Ensure index exists
if INDEX_NAME not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # all-MiniLM-L6-v2 embedding size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the Pinecone index
index = pc.Index(INDEX_NAME)

# Process documents
documents = load_documents(DIRECTORY_PATH)
chunked_docs = chunk_documents(documents)

# Insert document chunks into Pinecone
vector_data = [
    {
        "id": f"doc_{i}",
        "values": get_embedding(chunk.page_content),  # Generate embedding
        "metadata": {"text": chunk.page_content}
    }
    for i, chunk in enumerate(chunked_docs)
]

index.upsert(vectors=vector_data)
time.sleep(2)  # Allow indexing time

# Search function
def search_pinecone(query, top_k=5):
    query_embedding = get_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    print("\n🔍 Search Results:")
    for match in results.matches:
        print(f"\nScore: {match.score}")
        print(f"Text: {match.metadata['text']}")

# Example search
query_text = "what is Nationalism and Imperialism?"
search_pinecone(query_text, top_k=5)
