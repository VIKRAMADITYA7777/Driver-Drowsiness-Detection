import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.reports import generate_csv_report


def main(window_minutes: int = 60):
    path = generate_csv_report(window_minutes=window_minutes)
    print(f"Report generated: {path}")


if __name__ == '__main__':
    mins = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    main(mins)
