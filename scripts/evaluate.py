from scripts.rag_qa import retrieve_chunks, generate_answer, get_history
import statistics

TEST_CASES = [
    {"query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?", "expected": "শুম্ভুনাথ", "lang": "bn"},
    {"query": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?", "expected": "মামাকে", "lang": "bn"},
    {"query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "expected": "১৫ বছর", "lang": "bn"},
]

def evaluate():
    grounded_count = 0
    similarities = []
    for case in TEST_CASES:
        retrieved = retrieve_chunks(case["query"])
        history = get_history("eval_user")
        answer, grounded = generate_answer(case["query"], retrieved, history, case["lang"])
        if grounded:
            grounded_count += 1
        similarities.extend([score for _, score, _ in retrieved if score > 0.5])
        print(f"Query: {case['query']}\nAnswer: {answer}\nGrounded: {grounded}\nExpected in answer: {case['expected'] in answer}\n")

    groundedness = (grounded_count / len(TEST_CASES)) * 100
    avg_sim = statistics.mean(similarities) if similarities else 0
    print(f"Groundedness: {groundedness}%")
    print(f"Average Relevance (Cosine): {avg_sim:.2f}")

if __name__ == "__main__":
    evaluate()