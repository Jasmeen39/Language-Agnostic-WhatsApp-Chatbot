# ============================================
# utils/embeddings.py
# --------------------------------------------
# Handles creation of Hugging Face embeddings
# for text and document chunks
# ============================================

from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Initialize and return a HuggingFaceEmbeddings model.

    Args:
        model_name (str): Name or path of the sentence transformer model.

    Returns:
        HuggingFaceEmbeddings: Embedding model instance.
    """
    print(f" Loading embedding model: {model_name} ...")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print(" Embedding model loaded successfully.")
    return embeddings
