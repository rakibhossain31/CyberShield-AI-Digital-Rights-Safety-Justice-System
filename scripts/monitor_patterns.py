from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cybershield_ai.monitoring.pattern_monitor import build_pattern_report, write_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="artifacts/cybershield.db")
    parser.add_argument("--output", default="artifacts/pattern_report.json")
    args = parser.parse_args()
    report = build_pattern_report(args.db)
    write_report(report, args.output)
    print(f"Pattern report written to {args.output}")


if __name__ == "__main__":
    main()
