import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, TextLoader, PyPDFLoader

# Directory where files are stored
DIRECTORY_PATH = "data/"  # Change this to your directory path

# Function to detect file type and load using the appropriate loader
def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {filename}...")

        # Selecting the appropriate loader
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            print(f"Skipping unsupported file: {filename}")
            continue

        # Load the file
        docs = loader.load()  # Returns a list of Documents

        # Check if documents were loaded
        if docs:
            print(f"Loaded {len(docs)} documents from {filename}")
            documents.extend(docs)  # Ensure proper appending
        else:
            print(f"Warning: No content found in {filename}!")

    return documents

# Function to split documents into chunks of 1000 characters
def chunk_documents(documents, chunk_size=1000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return chunks

def load_and_chunk_documents(directory_path):
    docs = load_documents(directory_path)
    chunked_docs = chunk_documents(docs)
    return chunked_docs

# if __name__ == "__main__":
#     docs = load_documents(DIRECTORY_PATH)

#     # Debugging: Print number of documents loaded
#     print(f"Total documents loaded: {len(docs)}")
#     print(docs)
    
#     if docs:
#         chunked_docs = chunk_documents(docs)
#         print(f"Total chunks created: {len(chunked_docs)}")
        
#         # Print first 3 chunks for debugging
#         for i, chunk in enumerate(chunked_docs):
#             print(f"\nChunk {i+1}: {chunk.page_content}\n")
