# ============================================
# utils/retriever.py
# --------------------------------------------
# Builds and returns a Qdrant retriever from
# document chunks and embedding model
# ============================================

from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_retriever(chunks, embeddings, use_remote=False, collection_name="chatbot_docs"):
    """
    Create and return a Qdrant retriever (in-memory or remote).

    Args:
        chunks (list): List of LangChain Document chunks.
        embeddings (HuggingFaceEmbeddings): Embedding model.
        use_remote (bool): Whether to connect to a remote Qdrant instance.
        collection_name (str): Name of the Qdrant collection.

    Returns:
        retriever: Qdrant retriever object for use in RetrievalQA.
    """

    if use_remote:
        # ------------------------------------
        # Remote Qdrant setup (cloud-hosted)
        # ------------------------------------
        QDRANT_URL = os.getenv("QDRANT_URL")
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

        if not QDRANT_URL or not QDRANT_API_KEY:
            raise ValueError(" Remote Qdrant credentials missing in .env file!")

        print(f" Connecting to remote Qdrant: {QDRANT_URL}")
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

        qdrant = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            client=client,
            collection_name=collection_name
        )

    else:
        # ------------------------------------
        # In-memory Qdrant setup (local)
        # ------------------------------------
        print(" Using in-memory Qdrant instance...")
        qdrant = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            location=":memory:",  # No server needed
            collection_name=collection_name
        )

    print(" Qdrant retriever initialized successfully.")
    return qdrant.as_retriever()
