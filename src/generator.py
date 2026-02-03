import ollama

def generate_answer(query, contexts):
    context_text = "\n".join(contexts)

    prompt = f"""
Answer based ONLY on context.

Context:
{context_text}

Question:
{query}

Answer:
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']
