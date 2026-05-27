from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cybershield_ai.core import database


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--db", default="artifacts/cybershield.db")
    parser.add_argument("--output", default="artifacts/case_packet.md")
    args = parser.parse_args()
    case = database.get_case(args.db, args.case_id)
    if not case:
        raise SystemExit(f"Case {args.case_id} not found")
    payload = json.loads(case.get("payload_json") or "{}")
    md = f"""# CyberShield AI Case Packet

Case ID: {case['case_id']}

Category: {case['category']}

Priority: {case['priority']}

Risk score: {case['risk_score']}

## Redacted statement

{case['redacted_statement']}

## Complaint draft

{case['complaint_draft']}

## Awareness tips

"""
    for tip in payload.get("awareness_tips", []):
        md += f"- {tip}\n"
    md += "\n## Disclaimer\n\nThis packet is for human review only and is not legal advice.\n"
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"Case packet written to {out}")


if __name__ == "__main__":
    main()
