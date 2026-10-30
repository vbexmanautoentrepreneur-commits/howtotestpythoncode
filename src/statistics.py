from typing import Any


def compute_statistics(results: list[dict[str, Any]]) -> dict[str, float]:

    total = len(results)

    passed = sum(
        1 for test in results
        if test["status"] == "PASS"
    )

    failed = sum(
        1 for test in results
        if test["status"] == "FAIL"
    )

    success_rate = (
        passed / total * 100
        if total > 0 else 0.0
    )

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "success_rate": round(success_rate, 2)
    }