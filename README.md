This repository implements a basic Retrieval-Augmented Generation (RAG) pipeline for handling English and Bangla (Bengali) queries based on the "HSC26 Bangla 1st paper" PDF corpus. It supports text extraction, chunking, vectorization, retrieval, generation with memory, a REST API, and evaluation. This version uses Google's Gemini API for generation.

## Setup Guide

1. **Clone the Repository**:
git clone https://github.com/yourusername/simple-multilingual-rag.git
cd simple-multilingual-rag
text2. **Install Dependencies**:
pip install -r requirements.txt
text3. **Configure LLM**:
- Edit `config.yaml` to set your LLM provider.
- For Gemini: Set `llm_provider: gemini`, `model: gemini-1.5-flash` (or `gemini-pro`), and `google_api_key: your_key_here` (obtain from https://ai.google.dev/).
- Fallback dummy mode: Set `llm_provider: dummy` for testing without API (returns echoed context).

4. **Prepare the Knowledge Base**:
- Place the corpus PDF in `data/hsc26_bangla_1st_paper.pdf` (download from sources like ebookbou.edu.bd for "Aporichita" story).
- For testing without PDF, use the provided dummy `data/extracted_text.txt`.
- Run extraction: `python scripts/extract_text.py` (skippable with dummy).
- Run chunking and indexing: `python scripts/chunk_and_index.py`

5. **Run the API**:
uvicorn scripts.query_api:app --reload
text- Access at http://localhost:8000/docs for Swagger UI.

6. **Evaluate**:
python scripts/evaluate.py
text## Used Tools, Libraries, Packages
- **PDF Extraction**: PyMuPDF (fitz) for Unicode/Bangla support.
- **Chunking & RAG Pipeline**: LangChain for orchestration.
- **Embeddings**: sentence-transformers ('paraphrase-multilingual-mpnet-base-v2') for multilingual support.
- **Vector DB**: FAISS for local, efficient similarity search.
- **LLM**: LangChain with Google Gemini API; dummy fallback.
- **API**: FastAPI for REST endpoints.
- **Other**: unicodedata for normalization, pytest for tests, langchain-google-genai for Gemini.

## Sample Queries and Outputs (Bangla & English)
### Bangla Samples
- Query: "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
- Output: {"answer": "শুম্ভুনাথ", "sources": [{"chunk_id": "chunk_0", "score": 0.85, "text": "...relevant text..."}], "grounded": true}

- Query: "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?"
- Output: {"answer": "মামাকে", "sources": [...], "grounded": true}

- Query: "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
- Output: {"answer": "১৫ বছর", "sources": [...], "grounded": true}

### English Samples
- Query: "Who is referred to as handsome in Anupam's words?"
- Output: {"answer": "Shumbhunath", "sources": [...], "grounded": true}

- Query: "What is the real age of Kalyani at the time of marriage?"
- Output: {"answer": "15 years", "sources": [...], "grounded": true}

## API Documentation
- **Endpoint**: POST /api/query
- **Request Body** (JSON):
{
"user_id": "user123",
"query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
"lang": "bn"  // or "en"
}
text- **Response** (JSON):
{
"answer": "শুম্ভুনাথ",
"sources": [
{"chunk_id": "chunk_1", "score": 0.85, "text": "Excerpt from document..."}
],
"grounded": true
}
text- Usage Example (curl):
curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d '{"user_id": "user123", "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?", "lang": "bn"}'

- Usage Example (Python):
```python
- Usage Example (Python):
```python
import requests
response = requests.post("http://localhost:8000/api/query", json={"user_id": "user123", "query": "Query here", "lang": "bn"})
print(response.json())

Evaluation Matrix
Run evaluate.py for a report. Example output (with dummy corpus):

Groundedness: 100% (3/3 test cases grounded)
Average Relevance (Cosine Similarity): 0.82
Human-Labeled Examples: 3 samples, all pass (answer contains expected string).