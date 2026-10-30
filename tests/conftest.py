import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def pytest_sessionfinish(session, exitstatus):

    total = session.testscollected
    equal=120
    print("\n" + "=" * equal)
    print(f"🧪 Tests collected : {total}")

    if exitstatus == 0:
        print("✅ Status : SUCCESS")
        print(f"🎯 Reliability : 100% ({total}/{total})")
    else:
        print("❌ Status : FAILED")

    print("=" * equal)