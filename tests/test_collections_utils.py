from src.collections_utils import (find_duplicates)

def test_no_duplicate():
    assert find_duplicates(["A", "B"]) == []

def test_duplicates():
    result = find_duplicates(["A", "B", "A", "B"])
    assert set(result) == {"A", "B"}
