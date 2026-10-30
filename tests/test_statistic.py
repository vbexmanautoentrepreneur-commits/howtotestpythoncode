from src.statistics import compute_statistics

def test_empty_list():
    result = compute_statistics([])
    assert result == {"total": 0, "passed": 0, "failed": 0, "success_rate": 0.0}

def test_one_pass():
    result = compute_statistics([{"name": "test_a", "status": "PASS"}])
    assert result["total"] == 1
    assert result["passed"] == 1
    assert result["failed"] == 0
    assert result["success_rate"] == 100.0


def test_mixed_results():
    results = [
        {"name": "test1", "status": "PASS"},
        {"name": "test2", "status": "PASS"},
        {"name": "test3", "status": "FAIL"},
        {"name": "test4", "status": "PASS"},
    ]
    stats = compute_statistics(results)
    assert stats == {"total": 4, "passed": 3, "failed": 1, "success_rate": 75.0}