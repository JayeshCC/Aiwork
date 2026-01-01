from aiwork.core.memory import VectorMemory


def test_vector_memory_search_returns_matches():
    memory = VectorMemory()
    memory.add("hello world")
    memory.add("hello there")
    memory.add("unrelated text")

    results = memory.search("hello", k=2)
    assert len(results) == 2
    assert all("hello" in r["text"] for r in results)


def test_vector_memory_search_no_match():
    memory = VectorMemory()
    memory.add("alpha beta")
    results = memory.search("gamma", k=2)
    assert results == []
