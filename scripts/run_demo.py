from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cybershield_ai.core.models import IncidentReport
from cybershield_ai.core import database
from cybershield_ai.services.victim_advocate import VictimAdvocate
from cybershield_ai.services.evidence_vault import EvidenceVault
from cybershield_ai.monitoring.pattern_monitor import build_pattern_report, write_report

DB_PATH = "artifacts/cybershield.db"


def main():
    database.init_db(DB_PATH)
    advocate = VictimAdvocate(db_path=DB_PATH)
    vault = EvidenceVault(db_path=DB_PATH)
    results = []
    with open("data/demo/sample_incidents.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            report = IncidentReport(
                reporter_alias=row["case_id"],
                statement=row["statement"],
                location=row["location"],
                platform=row["platform"],
                suspect_identifier=row["suspect_identifier"],
                evidence_items=[row["evidence_name"]],
                wants_legal_aid=True,
                immediate_danger="leak" in row["statement"].lower(),
            )
            result = advocate.triage(report, case_id=row["case_id"])
            vault.add_text_evidence(result.case_id, row["evidence_name"], "Synthetic evidence text for demo only.")
            results.append(result.model_dump())

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/demo_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    report = build_pattern_report(DB_PATH)
    write_report(report, "artifacts/pattern_report.json")
    print("CyberShield demo completed.")
    print("Created artifacts/demo_results.json and artifacts/pattern_report.json")
    print(f"Cases processed: {len(results)}")


if __name__ == "__main__":
    main()
