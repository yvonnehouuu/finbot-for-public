# Finbot

An AI-powered financial chatbot built with **LangChain and Groq LLM** that answers finance-related questions based on **Taiwan's financial market context**.

This project was originally designed to explore **Retrieval-Augmented Generation (RAG)** for financial knowledge retrieval, but the final implementation focuses on a **conversational chatbot system** integrated with the LINE Messaging API.

🔗 **Full project website:**
[https://sites.google.com/view/xiaomingsadventures/%E9%A6%96%E9%A0%81](https://sites.google.com/view/xiaomingsadventures/%E9%A6%96%E9%A0%81)

---

# Project Overview

Finbot is a financial assistant chatbot that allows users to ask finance-related questions through **LINE messaging**.

The system uses:

* **Groq LLM (Llama3)**
* **LangChain conversation memory**
* **Prompt engineering for finance knowledge**
* **Flask webhook server**
* **LINE Messaging API**

The chatbot is designed to respond in **Traditional Chinese** and provide explanations based on **Taiwan’s financial market environment**.

---

# System Architecture

```
User
 ↓
LINE Messaging API
 ↓
Flask Server (main.py)
 ↓
LangChain Chatbot
 ↓
Groq LLM (Llama3)
```

---

# Project Structure

```
Finbot
│
├── main.py        # LINE webhook server
├── chatbot.py     # Groq chatbot logic
├── ragchat.py     # Experimental RAG implementation
├── data/          # Financial documents for retrieval
├── requirements.txt
└── README.md
```

* **main.py** handles LINE webhook requests and forwards user questions to the chatbot. 
* **chatbot.py** creates the conversational AI using LangChain and Groq LLM. 
* **ragchat.py** experiments with a RAG pipeline using HuggingFace embeddings and Chroma vector database. 

---

# Key Features

* Financial question answering chatbot
* Traditional Chinese responses
* Context-aware conversation memory
* LINE Bot integration
* Prompt engineering for finance domain
* Experimental RAG pipeline

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/finbot-for-public.git
cd finbot-for-public
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
ACCESS_TOKEN=your_line_channel_access_token
SECRET_KEY=your_line_channel_secret
```

---

# Running the Bot

Start the Flask server:

```bash
python main.py
```

The server will listen for LINE webhook events and generate responses using the Groq chatbot.

---

# RAG Exploration (Experimental)

This project originally attempted to implement a **Retrieval-Augmented Generation system** using:

* HuggingFace embeddings
* Chroma vector database
* Financial document retrieval

However, due to implementation challenges in the vector database pipeline, the current version primarily focuses on the **chatbot architecture**.

---

# Related Project

This repository is part of the broader project:

**小明奇幻旅程 (Xiaoming’s Adventures)**

Project website:
[https://sites.google.com/view/xiaomingsadventures/%E9%A6%96%E9%A0%81](https://sites.google.com/view/xiaomingsadventures/%E9%A6%96%E9%A0%81)

The project explores the application of AI technologies in financial education and conversational assistants.

---

# Technologies Used

* Python
* LangChain
* Groq LLM
* Flask
* LINE Messaging API
* HuggingFace embeddings
* Chroma vector database

---

# Future Improvements

* Complete RAG knowledge retrieval pipeline
* Improve financial dataset integration
* Deploy chatbot to cloud infrastructure
* Add multilingual support



會比現在這版 **更像研究專案 / AI portfolio repo**。
