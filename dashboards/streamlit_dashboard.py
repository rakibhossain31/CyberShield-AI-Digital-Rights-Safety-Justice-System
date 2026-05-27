from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
import streamlit as st

from cybershield_ai.core import database
from cybershield_ai.monitoring.pattern_monitor import build_pattern_report

DB_PATH = os.getenv("CYBERSHIELD_DB_PATH", "artifacts/cybershield.db")

def read_table(table: str) -> pd.DataFrame:
    database.init_db(DB_PATH)
    import sqlite3
    with sqlite3.connect(DB_PATH) as conn:
        try:
            return pd.read_sql_query(f"SELECT * FROM {table}", conn)
        except Exception:
            return pd.DataFrame()

st.set_page_config(page_title="CyberShield AI Dashboard", layout="wide")
st.title("CyberShield AI Monitoring Dashboard")
st.caption("Safe demo dashboard. Use synthetic data only. Human review is required for all outputs.")

summary = database.summary(DB_PATH)
col1, col2, col3 = st.columns(3)
col1.metric("Cases", summary["case_count"])
col2.metric("Evidence hashes", summary["evidence_count"])
col3.metric("Feedback entries", summary["feedback_count"])

st.subheader("Case categories")
cat_df = pd.DataFrame(summary["categories"])
if not cat_df.empty:
    st.bar_chart(cat_df.set_index("category"))
else:
    st.info("No cases yet. Run `python scripts/run_demo.py` first.")

st.subheader("Priority distribution")
prio_df = pd.DataFrame(summary["priorities"])
if not prio_df.empty:
    st.bar_chart(prio_df.set_index("priority"))

st.subheader("Recent cases")
cases = read_table("cases")
if not cases.empty:
    st.dataframe(cases[["case_id", "created_at", "category", "risk_score", "priority", "platform", "location"]].tail(20), use_container_width=True)

st.subheader("Repeat pattern notes")
report = build_pattern_report(DB_PATH)
if report["risk_notes"]:
    for note in report["risk_notes"]:
        st.warning(note)
else:
    st.success("No high-repeat anonymized patterns detected in the demo database.")

st.subheader("Audit events")
audit = read_table("audit_events")
if not audit.empty:
    st.dataframe(audit.tail(30), use_container_width=True)
