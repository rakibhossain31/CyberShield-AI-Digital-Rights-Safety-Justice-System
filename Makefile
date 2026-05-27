.PHONY: install test demo api dashboard batch monitor

install:
	pip install -r requirements.txt

test:
	python -m pytest tests -q

demo:
	python scripts/run_demo.py

api:
	PYTHONPATH=src uvicorn cybershield_ai.api.main:app --host 0.0.0.0 --port 8000 --reload

dashboard:
	PYTHONPATH=src streamlit run dashboards/streamlit_dashboard.py

batch:
	python scripts/generate_synthetic_cases.py --rows 50 --output data/demo/synthetic_cases.csv
	python scripts/batch_triage.py --input data/demo/synthetic_cases.csv --output artifacts/batch_triage_results.csv

monitor:
	python scripts/monitor_patterns.py --db artifacts/cybershield.db --output artifacts/pattern_report.json
