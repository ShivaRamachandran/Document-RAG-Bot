Document RAG (Retrieval-Augmented Generation)

Overview:
This project implements a full-stack Retrieval-Augmented Generation (RAG) system using LangChain, Pinecone, and Gemini for LLM-based text generation. It provides a frontend built with React that allows users to query documents as well as manage the RAG dataset (add, delete, and list documents).

Features:
1. Efficient Chunking: Uses Recursive Character Tokenization via RecursiveCharacterTextSplitter (LangChain), ideal for unstructured text (PDFs, DOCX, TXT) while preserving context.
2. Semantic Search: Embeddings generated using sentence-transformers/all-MiniLM-L6-v2.
3. Vector Storage: Uses Pinecone for vector database storage and retrieval.
4. LLM-Based Generation: Uses Gemini-1.5-Flash for fast and accurate text generation.
5. User-Friendly Frontend: Built with React, featuring options to query documents, add new RAG documents, delete existing ones, and list all stored documents.


Tech Stack-

Backend:
LangChain (for chunking & retrieval)
SentenceTransformers (for embeddings)
Pinecone (for vector storage & search)
Gemini-1.5-Flash (for LLM-based completions)
FastAPI / Flask (for API development)

Frontend:
React (for UI development)
Axios (for API requests)

