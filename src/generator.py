import ollama

import requests

def generate_answer(query, contexts):
    prompt = f"""
প্রশ্ন: {query}

তথ্য:
{contexts}

সংক্ষিপ্ত ও সঠিক উত্তর দাও:
"""
    r = requests.post("http://localhost:11434/api/generate",
        json={"model":"mistral","prompt":prompt,"stream":False})
    return r.json()["response"]

