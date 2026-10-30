from src.strings import  build_greeting, normalize_name

def test_build_greeting():
    assert build_greeting("Bob") == "Hello Bob"

def test_normalize_name():
    assert normalize_name(" bob ") == "BOB"

def test_normalize_empty():
    assert normalize_name("") == ""