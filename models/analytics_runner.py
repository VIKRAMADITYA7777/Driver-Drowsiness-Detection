import time
from pathlib import Path
from app.database import SessionLocal
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.analytics import snapshot_and_store


def main(interval_seconds: int = 300):
    print(f"Starting analytics runner with interval {interval_seconds}s")
    while True:
        snapshot_and_store(window_minutes=5)
        print("Snapshot stored")
        time.sleep(interval_seconds)


if __name__ == '__main__':
    main()
