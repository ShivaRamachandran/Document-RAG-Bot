import os
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from utils import load_and_chunk_documents, DIRECTORY_PATH
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "docu-rag"
DIMENSION = 350  # all-MiniLM-L6-v2 embedding size

# Ensure the index exists
existing_indexes = pc.list_indexes().names()
if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    time.sleep(5)  # Allow time for index creation

# Connect to the index
index = pc.Index(INDEX_NAME)

# Load and chunk documents
chunked_docs = load_and_chunk_documents(DIRECTORY_PATH)
print(f"Total Chunks Generated: {len(chunked_docs)}")

# Load Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Convert chunks into embeddings
document_chunks = [doc.page_content for doc in chunked_docs]
embeddings = model.encode(document_chunks, show_progress_bar=True)

# Store vectors in Pinecone
vector_data = [
    {
        "id": f"chunk_{i}",
        "values": embeddings[i].tolist(),
        "metadata": {"text": chunk.page_content},
    }
    for i, chunk in enumerate(chunked_docs)
]

index.upsert(vectors=vector_data)
time.sleep(2)  # Allow indexing time

print("Embeddings stored in Pinecone successfully!")

# Search function
def search_pinecone(query, top_k=5):
    query_embedding = model.encode([query])[0].tolist()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    retrieved_chunks = []
    
    if results.matches:
        for match in results.matches:
            retrieved_chunks.append(match.metadata["text"])  # Store relevant text chunks
    
    return "\n".join(retrieved_chunks) if retrieved_chunks else "No relevant information found."