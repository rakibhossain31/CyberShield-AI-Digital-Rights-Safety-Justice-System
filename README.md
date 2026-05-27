# CyberShield AI: Digital Rights, Safety and Justice Support System

CyberShield AI is a safe, portfolio-ready demonstration of an AI-assisted cyber safety and digital rights workflow. It is designed to show how victim-centered reporting, structured complaint drafting, evidence hashing, repeat-pattern detection, awareness guidance, monitoring, and audit logging can work together in a responsible system.

> Important: This project is a technical prototype and education/demo system. It is not legal advice, does not submit FIRs or complaints to any authority, does not identify real offenders, and must not be used with real victim data without legal, security, and ethics review.

## What the system does

1. Accepts a cyber incident report from a victim or support worker.
2. Redacts sensitive information from text for safer processing.
3. Classifies the case type: harassment, hacking, blackmail, impersonation, doxxing, financial fraud, or other.
4. Scores urgency and escalation risk.
5. Retrieves relevant guidance from a small local knowledge base.
6. Generates a structured complaint/FIR-style draft for human review.
7. Stores evidence hashes with timestamps and a hash-chain audit ledger.
8. Detects repeat patterns using anonymized suspect identifiers.
9. Produces awareness guidance and next-step checklists.
10. Logs cases, evidence, feedback, and audit events in SQLite.
11. Provides FastAPI endpoints, a Streamlit dashboard, scripts, Docker, and CI tests.

## Quick start

```bash
cd CyberShield-AI-Digital-Rights-Safety-Justice-System
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_demo.py
```

Start the API:

```bash
PYTHONPATH=src uvicorn cybershield_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
uvicorn cybershield_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Start the dashboard:

```bash
PYTHONPATH=src streamlit run dashboards/streamlit_dashboard.py
```

## Common commands

```bash
python scripts/generate_synthetic_cases.py --rows 50 --output data/demo/synthetic_cases.csv
python scripts/batch_triage.py --input data/demo/synthetic_cases.csv --output artifacts/batch_triage_results.csv
python scripts/monitor_patterns.py --db artifacts/cybershield.db --output artifacts/pattern_report.json
python scripts/export_case_packet.py --case-id CASE_ID_HERE --output artifacts/case_packet.md
pytest -q
```

## API endpoints

| Endpoint | Method | Purpose |
|---|---:|---|
| `/health` | GET | Service health check |
| `/triage` | POST | Classify report, score risk, generate complaint draft |
| `/evidence/text` | POST | Hash text evidence and add it to the chain-of-custody ledger |
| `/case/{case_id}` | GET | Retrieve stored case result |
| `/patterns` | GET | View anonymized repeat-pattern summary |
| `/feedback` | POST | Log reviewer/victim support feedback |
| `/dashboard/summary` | GET | Metrics for dashboard |

## Project structure

```text
src/cybershield_ai/       Core application package
scripts/                  CLI scripts for demo, batch processing, monitoring, export
dashboards/               Streamlit dashboard
data/demo/                Synthetic demo data and local knowledge base
artifacts/                Generated outputs, SQLite DB, reports
tests/                    Automated tests
.github/workflows/        GitHub Actions CI
```

## Safety rules
- Keep all legal outputs human-reviewed.
- Treat model outputs as support, not decisions.
- Replace the demo legal knowledge base with verified legal content before any real deployment.

## Recruiter-facing summary

This project demonstrates AI product engineering, backend APIs, privacy-aware NLP, RAG-style retrieval, digital evidence integrity, monitoring, auditability, and safety-by-design for a sensitive public-interest use case.
