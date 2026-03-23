# ================================
# Language-Agnostic Chatbot (Terminal Prototype)
# Now supports Indian languages via translation
# ================================

from langdetect import detect
from googletrans import Translator
from deep_translator import GoogleTranslator
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from dotenv import load_dotenv
import os
#import asyncio

# ------------------------------------
# 1. Load environment variables
# ------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(" Please set your GROQ_API_KEY in the .env file!")

# ------------------------------------
# 2. Initialize the LLM (Groq)
# ------------------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
)

# ------------------------------------
# 3. Load datasets (.txt and .pdf)
# ------------------------------------
data_folder = "data"

text_docs = []
pdf_docs = []

# Load text files
for file in os.listdir(data_folder):
    if file.lower().endswith(".txt"):
        loader = TextLoader(os.path.join(data_folder, file))
        text_docs.extend(loader.load())

# Load PDF files
for file in os.listdir(data_folder):
    if file.lower().endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(data_folder, file))
        pdf_docs.extend(loader.load())

# Combine all documents
docs = text_docs + pdf_docs
print(f" Loaded {len(docs)} documents from {data_folder}")

# ------------------------------------
# 4. Split into chunks
# ------------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} text chunks")

# ------------------------------------
# 5. Create embeddings
# ------------------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ------------------------------------
# 6. Setup Qdrant (in-memory vector store)
# ------------------------------------
qdrant = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    location=":memory:",       # In-memory store
    collection_name="chatbot_docs"
)

# ------------------------------------
# 7. Build Retrieval-QA Chain
# ------------------------------------
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=qdrant.as_retriever()
)

# ------------------------------------
# 8. Define multilingual Q&A function (with translation)
# ------------------------------------
translator = Translator()

def ask_user(user_input: str) -> str:
    try:
        lang = detect(user_input)
    except Exception:
        lang = "en"  # fallback if detection fails

    # Translate input to English (if not already English)
    if lang != "en":
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
    else:
        translated_input = user_input

    # Ask the model (in English)
    instruction = f"Please reply in English, but we'll later translate back to {lang}.\n\n"
    query = instruction + translated_input
    response = qa.invoke({"query": query})
    answer = response["result"] if isinstance(response, dict) and "result" in response else response

    # Translate answer back to user's original language
    if lang != "en":
        translated_output = GoogleTranslator(source='en', target=lang).translate(answer)
    else:
        translated_output = answer

    return translated_output


# # ------------------------------------
# # 9. Chat loop (Terminal-based)
# # ------------------------------------
# print("\n Multilingual Chatbot is ready!")
# print("Type your question (type 'exit' to quit)\n")

# while True:
#     user_input = input("You: ").strip()
#     if user_input.lower() in ["exit", "quit"]:
#         print(" Goodbye!")
#         break

#     answer = ask_user(user_input)
#     print(f"Bot: {answer}\n")
