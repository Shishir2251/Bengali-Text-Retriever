
### DECISIONS.md
```markdown
# Design Decisions & Justifications

1. **Text Extraction Method/Library**: Used PyMuPDF (fitz) because it handles Bangla Unicode well and preserves layout. Challenges: Broken lines and hyphenation in PDF; resolved by joining lines and removing hyphens during cleaning.

2. **Chunking Strategy**: Paragraph-based with 200-token overlap (using NLTK for tokenization). Good for semantic retrieval as it preserves context in narrative texts like books, reducing split meanings.

3. **Embedding Model**: 'paraphrase-multilingual-mpnet-base-v2' from sentence-transformers. Chosen for multilingual support (including Bangla); captures meaning via transformer-based semantic encoding, handling paraphrases across languages.

4. **Query-Chunk Comparison**: Cosine similarity via FAISS (flat index for small corpus). Chosen for efficiency and effectiveness in dense vector search; local storage avoids cloud costs.

5. **Meaningful Comparison**: Embed query in same space as chunks; use multilingual model for cross-lang. If vague/missing context, retrieval scores low (<0.5 threshold), trigger fallback showing top chunks.

6. **Results Relevance**: Yes, relevant for samples (high scores). Improvements: Finer chunking, better model like mBERT fine-tuned on Bangla, or larger corpus.