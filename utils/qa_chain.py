# ============================================
# utils/qa_chain.py
# --------------------------------------------
# Builds the RetrievalQA chain and defines the
# multilingual Q&A function for the chatbot
# ============================================

from langdetect import detect
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def create_qa_chain(retriever):
    """
    Create and return a RetrievalQA chain using Groq LLM.

    Args:
        retriever: Qdrant retriever instance.

    Returns:
        RetrievalQA: LangChain QA chain for answering questions.
    """

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError(" Please add GROQ_API_KEY to your .env file!")

    print(" Initializing Groq LLM model...")
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="meta-llama/llama-4-maverick-17b-128e-instruct"
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    print(" RetrievalQA chain initialized successfully.")
    return qa


def ask_user(query: str, qa_chain) -> str:
    """
    Handles multilingual user input and returns an AI response.

    Args:
        query (str): The user’s question.
        qa_chain (RetrievalQA): The RetrievalQA chain.

    Returns:
        str: The chatbot’s multilingual response.
    """

    # Detect language of user input
    try:
        lang = detect(query)
    except Exception:
        lang = "en"

    # Add instruction to maintain same language in response
    instruction = f"Please reply in the same language as the user input ({lang}).\n\n"
    formatted_query = instruction + query

    # Run through the QA chain
    response = qa_chain.invoke({"query": formatted_query})

    # Extract clean result
    if isinstance(response, dict) and "result" in response:
        return response["result"]
    return str(response)
