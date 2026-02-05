import requests
import re

def clean_chunks(chunks):
    """
    Remove MCQ noise and keep only meaningful Bangla sentences
    """
    clean = []

    for chunk in chunks:
        chunk = chunk.replace("\n", " ")

        # Remove MCQ patterns like (ক) (খ) [ঢা.বো.' ১৬]
        chunk = re.sub(r"\(.*?\)", "", chunk)
        chunk = re.sub(r"\[.*?\]", "", chunk)

        # Split into Bangla sentences
        sentences = chunk.split("।")

        for s in sentences:
            s = s.strip()

            # Keep only useful length sentences
            if len(s) > 25:
                clean.append(s)

    return "। ".join(clean) + "।"


def generate_answer(query, chunks):
    """
    Generate exact answer from cleaned context
    """
    context = clean_chunks(chunks)

    prompt = f"""
প্রশ্ন: {query}

তথ্য:
{context}

সংক্ষিপ্ত, সঠিক এবং স্পষ্ট উত্তর দাও।
শুধুমাত্র সরাসরি উত্তর দাও, কোন ব্যাখ্যা বা গল্প নয়।
১–২ লাইনে দাও:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return response.json()["response"].strip()

    except Exception as e:
        print("Generator error:", e)
        return ""
