from src.json_tools import (remove_empty_keys, count_keys,)

def test_remove_empty_key():

    data = {"name": "Bob", "": "invalid"}
    result = remove_empty_keys(data)
    assert result == {"name": "Bob"}


def test_count_keys():

    data = {"A": {"B": {"C": 1}}}
    assert count_keys(data) == 3

def test_real_case():
    data = {"name": "Emmanuel", "address": {"city": "Caen", "zip": "14000"}, "skills": {"python": True, "qt": True}}
    assert count_keys(data) == 7