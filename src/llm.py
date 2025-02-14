import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGroq
from langchain import PromptTemplate
from src.template import template

# Load API key from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# Initialize the Gemini model using Groq
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="gemini-1.5-flash"  # Use "gemini-1.5-pro" for better performance
)


# Initialize the prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# Example document chunks (simulated)
document_chunks = [
    "Neural networks suffer from overfitting when they memorize training data instead of generalizing patterns.",
    "Regularization techniques like dropout and L2 regularization help reduce overfitting.",
]

# Combine chunks into context
context = "\n".join(document_chunks) if document_chunks else "No relevant information available."

# Define user query
user_question = "How can we prevent overfitting in neural networks?"

# Format the final prompt
formatted_prompt = prompt.format(context=context, question=user_question)

# Get response from the LLM
response = llm.invoke(formatted_prompt)

print("LLM Response:", response)
