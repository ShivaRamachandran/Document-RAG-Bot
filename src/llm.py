import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from vectordatabase import search_pinecone 


log_file = "logs.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# Validate API key
if not gemini_api_key:
    logging.error("GEMINI_API_KEY is not set or incorrect/invalid in the environment variables, Please check it.")
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")  # Change to "gemini-1.5-pro" if needed

# Define a prompt template
template = """You are an AI assistant that answers user queries based only on the provided documents.

If the documents contain relevant information, provide an accurate response or summary.
If the information is not available in the documents, respond with: "Sorry, your query has no matching answer from the documents. Try something else."

Context: {context}
Question: {question}
Answer:
"""
def generate_response(user_question):
    logging.info(f"Received user query: {user_question}")
    # Retrieve relevant chunks from Pinecone
    context = search_pinecone(user_question, top_k=5)
    # logging.info(f"Retrieved context from Pinecone: {context}")

    # Format the prompt
    formatted_prompt = template.format(context=context, question=user_question)

    # # Get response from Gemini API
    # response = model.generate_content(formatted_prompt)

    # return response.text.strip()
    try:
        response = model.generate_content(formatted_prompt)
        llm_response = response.text.strip()
        logging.info(f"BOT Generated response: {llm_response}")
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        llm_response = "Error generating response."

    return llm_response

if __name__ == "__main__":
    # Example query
    user_query = "Balkans was a region of geographical and ethnic variation comprising modern-day of what?"
    response = generate_response(user_query)
    
    print("\n🔍 LLM Response:\n", response)

