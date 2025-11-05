from utils.embedder import Embedder
from utils.vector_store import query_similar
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"   # Or another Groq-supported model

embedder = Embedder()

def generate_answer(query):
    query_vector = embedder.get_embedding(query)
    try:
        docs = query_similar(query_vector)
    except Exception as e:
        print("⚠️ Vector search error:", e)
        docs = []

    context = "\n".join([doc.get("content", "") for doc in docs]) or "No relevant context found."

    prompt = f"""
You are a helpful assistant. Use only the following context to answer the question clearly.

Context:
{context}

Question: {query}
Answer:
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print("❌ LLM API error:", response.status_code, response.text)
            return f"Error from LLM API: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("🔥 Exception in Groq request:", e)
        return f"Error contacting Groq API: {e}"
