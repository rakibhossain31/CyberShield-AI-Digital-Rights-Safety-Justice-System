from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
from cybershield_ai.core import database


def build_pattern_report(db_path: str = database.DEFAULT_DB_PATH) -> Dict[str, Any]:
    summary = database.summary(db_path)
    risk_notes = []
    for item in summary["repeat_patterns"]:
        if item["case_count"] >= 3:
            risk_notes.append(f"Anonymized pattern {item['anonymized_suspect_key']} appears in {item['case_count']} cases.")
    return {"summary": summary, "risk_notes": risk_notes, "generated_at": database.utc_now()}


def write_report(report: Dict[str, Any], output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    html_path = path.with_suffix(".html")
    html_path.write_text(
        "<html><body><h1>CyberShield AI Pattern Report</h1><pre>" +
        json.dumps(report, indent=2, ensure_ascii=False) +
        "</pre></body></html>",
        encoding="utf-8",
    )
