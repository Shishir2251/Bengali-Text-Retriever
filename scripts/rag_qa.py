from sentence_transformers import SentenceTransformer
import faiss
import pickle
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import List, Dict, Tuple
import numpy as np

INDEX_PATH = "data/faiss_index.index"
CHUNKS_PATH = "data/chunks.pkl"
CONFIG_PATH = "config.yaml"
SHORT_TERM_MEMORY_LIMIT = 5

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

embedder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

llm = ChatGoogleGenerativeAI(model=config["model"], google_api_key=config["google_api_key"])

memory_store: Dict[str, List[Dict[str, str]]] = {}

def load_index_and_chunks() -> Tuple[faiss.Index, List[str]]:
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

index, chunks = load_index_and_chunks()

def retrieve_chunks(query: str, top_k: int = 5) -> List[Tuple[str, float, int]]:
    query_emb = embedder.encode([query])
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
    distances, indices = index.search(query_emb, top_k)
    results = []
    for cos, idx in zip(distances[0], indices[0]):
        if idx == -1: continue
        results.append((chunks[idx], cos, idx))
    return results

def get_history(user_id: str) -> str:
    if user_id not in memory_store:
        memory_store[user_id] = []
    history = memory_store[user_id][-SHORT_TERM_MEMORY_LIMIT:]
    return "\n".join([f"Q: {turn['query']}\nA: {turn['answer']}" for turn in history])

def generate_answer(query: str, retrieved: List[Tuple[str, float, int]], history: str, lang: str, user_id: str) -> Tuple[str, bool]:
    context = "\n\n".join([chunk for chunk, _, _ in retrieved])
    max_score = max([score for _, score, _ in retrieved]) if retrieved else 0
    if max_score < 0.3:
        return f"I couldn't find a supported answer in the documents. Top chunks:\n{context}", False

    prompt_template = PromptTemplate(
        input_variables=["history", "context", "query"],
        template="History: {history}\nContext: {context}\nQuery: {query}\nExtract the short answer (e.g., name 'শুম্ভুনাথ' or number '১৫') from the context or MCQ options. If MCQ, select the correct option letter (e.g., (ঘ) শুম্ভুনাথ) based on the query. If multiple, choose the best match. If not found, say 'Not found'. Answer in {lang}, direct and concise:"
    )
    prompt = prompt_template.format(history=history, context=context, query=query, lang="Bangla" if lang == "bn" else "English")

    answer = llm.invoke(prompt).content.strip()

    memory_store.setdefault(user_id, []).append({"query": query, "answer": answer})
    return answer, True