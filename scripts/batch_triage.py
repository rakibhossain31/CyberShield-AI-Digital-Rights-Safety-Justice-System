from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cybershield_ai.core.models import IncidentReport
from cybershield_ai.services.victim_advocate import VictimAdvocate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="artifacts/batch_triage_results.csv")
    parser.add_argument("--db", default="artifacts/cybershield.db")
    args = parser.parse_args()
    advocate = VictimAdvocate(db_path=args.db)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.input, newline="", encoding="utf-8") as f, out.open("w", newline="", encoding="utf-8") as g:
        reader = csv.DictReader(f)
        fields = ["case_id", "category", "confidence", "risk_score", "priority", "repeat_pattern_count", "anonymized_suspect_key"]
        wr = csv.DictWriter(g, fieldnames=fields)
        wr.writeheader()
        for row in reader:
            report = IncidentReport(
                reporter_alias=row.get("case_id", "batch_case"),
                statement=row["statement"],
                location=row.get("location"),
                platform=row.get("platform"),
                suspect_identifier=row.get("suspect_identifier"),
                evidence_items=[row.get("evidence_name", "evidence")],
            )
            result = advocate.triage(report, case_id=row.get("case_id") or None)
            wr.writerow({k: getattr(result, k) for k in fields})
    print(f"Batch triage written to {out}")


if __name__ == "__main__":
    main()
