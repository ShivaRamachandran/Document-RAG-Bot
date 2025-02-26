# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from llm import generate_response

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI server is running now!"}

# # CORS middleware for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Update with your frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/query")
# async def query_llm(question: str):
#     """Endpoint to handle user queries as a URL query parameter."""
#     try:
#         response = generate_response(question)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)


from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from llm import generate_response
import os

app = FastAPI()

# Directory to store RAG documents
DOCS_DIRECTORY = "D:/Projects/Sonata/POC2/data"
os.makedirs(DOCS_DIRECTORY, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running now!"}

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
async def query_llm(question: str):
    """Endpoint to handle user queries."""
    try:
        response = generate_response(question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new RAG document."""
    try:
        file_location = os.path.join(DOCS_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        return {"message": f"{file.filename} uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete")
async def delete_document(filename: str):
    """Delete a RAG document."""
    file_path = os.path.join(DOCS_DIRECTORY, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"{filename} deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

@app.get("/list_docs")
async def list_documents():
    """List all available RAG documents."""
    files = os.listdir(DOCS_DIRECTORY)
    return {"documents": files}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


