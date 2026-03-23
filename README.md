# 🌍 Language-Agnostic WhatsApp Chatbot

An AI-powered WhatsApp chatbot that can understand and respond in multiple languages.
It uses LLMs, embeddings, and translation to provide intelligent, context-aware answers.

---

## 🚀 Features

* 🌐 **Language Agnostic** – Supports multiple languages automatically
* 🤖 **AI-Powered Responses** – Uses Groq LLM for smart replies
* 🔎 **RAG (Retrieval-Augmented Generation)** – Answers based on your custom data
* 📄 **Supports PDFs & Text Files** – Extracts and learns from documents
* 💬 **WhatsApp Integration** – Send and receive messages via WhatsApp Cloud API

---

## 🛠️ Tech Stack

* Python
* Flask
* LangChain
* Groq API (LLM)
* HuggingFace Embeddings
* Qdrant (Vector Store)
* WhatsApp Cloud API
* Google Translate / langdetect

---

## 📂 Project Structure

```
.
├── app.py              # Webhook server (WhatsApp Cloud API)
├── main.py             # Core chatbot logic (RAG + LLM)
├── update.py           # Updates vector database
├── whatsappbot.py      # Manual message sending (testing)
├── data/               # Documents (PDFs, text files)
├── .env                # Environment variables (NOT uploaded)
├── .env.example        # Example environment variables
├── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/Language-Agnostic-WhatsApp-Chatbot.git
cd Language-Agnostic-WhatsApp-Chatbot
```

---

### 2. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup environment variables

Create a `.env` file:

```
WHATSAPP_TOKEN=your_token_here
PHONE_NUMBER_ID=your_phone_id_here
RECIPIENT_PHONE=your_phone_number_here
GROQ_API_KEY=your_groq_key_here
```

---

### 5. Run the chatbot

#### 👉 Option 1: Webhook (recommended)

```
python app.py
```

#### 👉 Option 2: Manual testing

```
python whatsappbot.py
```

---

## 📌 How It Works

1. User sends message on WhatsApp
2. Message is received via webhook
3. Language is detected
4. Input is translated to English
5. LLM processes query using RAG
6. Response is translated back
7. Reply is sent to user

---

## 🔐 Security Note

* `.env` is ignored to protect API keys
* Never expose your tokens publicly

---

## 🌟 Future Improvements

* Deploy on cloud (Render / AWS / GCP)
* Add voice message support
* Improve response accuracy with better datasets
* Add UI dashboard

---

## 👩‍💻 Author

Jasmeen Kaur

---

## ⭐ If you like this project

Give it a star on GitHub ⭐
