# ============================================
# utils/loader.py
# --------------------------------------------
# Handles loading of all .txt and .pdf datasets
# from the /data folder and returns combined docs
# ============================================

import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader

def load_documents(data_folder: str = "data"):
    """
    Loads all .txt and .pdf documents from the given folder.

    Args:
        data_folder (str): Path to folder containing data files.

    Returns:
        list: Combined list of LangChain Document objects.
    """

    if not os.path.exists(data_folder):
        raise FileNotFoundError(f" Data folder '{data_folder}' not found!")

    all_docs = []

    # Load all .txt files
    for file in os.listdir(data_folder):
        if file.lower().endswith(".txt"):
            try:
                loader = TextLoader(os.path.join(data_folder, file))
                all_docs.extend(loader.load())
                print(f" Loaded text file: {file}")
            except Exception as e:
                print(f" Error loading {file}: {e}")

    # Load all .pdf files
    for file in os.listdir(data_folder):
        if file.lower().endswith(".pdf"):
            try:
                loader = PyPDFLoader(os.path.join(data_folder, file))
                all_docs.extend(loader.load())
                print(f" Loaded PDF file: {file}")
            except Exception as e:
                print(f" Error loading {file}: {e}")

    print(f" Total documents loaded: {len(all_docs)}")
    return all_docs
