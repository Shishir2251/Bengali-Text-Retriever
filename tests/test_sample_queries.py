import pytest
from scripts.rag_qa import retrieve_chunks, generate_answer, get_history

TEST_CASES = [
    ("অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?", "শুম্ভুনাথ", "bn"),
    ("কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?", "মামাকে", "bn"),
    ("বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "১৫ বছর", "bn"),
]

@pytest.mark.parametrize("query,expected,lang", TEST_CASES)
def test_sample_queries(query, expected, lang):
    retrieved = retrieve_chunks(query)
    history = get_history("test_user")
    answer, grounded = generate_answer(query, retrieved, history, lang)
    assert grounded, "Should be grounded"
    assert expected in answer, f"Expected '{expected}' in '{answer}'"