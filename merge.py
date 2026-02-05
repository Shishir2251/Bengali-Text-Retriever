from src.retriever import retrieve
from src.generator import generate_answer

query = "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"

# Retrieve top 5 chunks
top_chunks = retrieve(query, k=5)

# Generate answer
answer = generate_answer(query, top_chunks)

print("Query:", query)
print("Answer:", answer)
