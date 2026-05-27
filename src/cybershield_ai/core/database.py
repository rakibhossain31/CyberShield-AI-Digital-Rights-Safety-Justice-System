from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

DEFAULT_DB_PATH = os.getenv("CYBERSHIELD_DB_PATH", "artifacts/cybershield.db")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def connect(db_path: str = DEFAULT_DB_PATH):
    ensure_parent(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with connect(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                reporter_alias TEXT,
                category TEXT,
                confidence REAL,
                risk_score INTEGER,
                priority TEXT,
                redacted_statement TEXT,
                platform TEXT,
                location TEXT,
                anonymized_suspect_key TEXT,
                repeat_pattern_count INTEGER,
                complaint_draft TEXT,
                payload_json TEXT
            );

            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                case_id TEXT,
                evidence_name TEXT,
                evidence_hash TEXT,
                chain_hash TEXT,
                previous_chain_hash TEXT,
                timestamp_utc TEXT,
                collector_alias TEXT,
                metadata_json TEXT
            );

            CREATE TABLE IF NOT EXISTS offender_patterns (
                anonymized_suspect_key TEXT PRIMARY KEY,
                first_seen TEXT,
                last_seen TEXT,
                case_count INTEGER,
                categories_json TEXT
            );

            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id TEXT PRIMARY KEY,
                case_id TEXT,
                reviewer_alias TEXT,
                rating INTEGER,
                useful INTEGER,
                notes TEXT,
                timestamp_utc TEXT
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT,
                case_id TEXT,
                timestamp_utc TEXT,
                details_json TEXT
            );
            """
        )


def insert_case(db_path: str, row: Dict[str, Any]) -> None:
    init_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO cases (
                case_id, created_at, reporter_alias, category, confidence, risk_score, priority,
                redacted_statement, platform, location, anonymized_suspect_key, repeat_pattern_count,
                complaint_draft, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["case_id"], row.get("created_at", utc_now()), row.get("reporter_alias"), row.get("category"),
                row.get("confidence"), row.get("risk_score"), row.get("priority"), row.get("redacted_statement"),
                row.get("platform"), row.get("location"), row.get("anonymized_suspect_key"), row.get("repeat_pattern_count", 0),
                row.get("complaint_draft"), json.dumps(row.get("payload", {}), ensure_ascii=False),
            ),
        )


def insert_evidence(db_path: str, row: Dict[str, Any]) -> None:
    init_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO evidence (
                evidence_id, case_id, evidence_name, evidence_hash, chain_hash,
                previous_chain_hash, timestamp_utc, collector_alias, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["evidence_id"], row["case_id"], row["evidence_name"], row["evidence_hash"],
                row["chain_hash"], row.get("previous_chain_hash"), row["timestamp_utc"],
                row.get("collector_alias", "demo_user"), json.dumps(row.get("metadata", {}), ensure_ascii=False),
            ),
        )


def last_chain_hash(db_path: str) -> str:
    init_db(db_path)
    with connect(db_path) as conn:
        cur = conn.execute("SELECT chain_hash FROM evidence ORDER BY timestamp_utc DESC LIMIT 1")
        row = cur.fetchone()
        return row["chain_hash"] if row else "GENESIS"


def get_case(db_path: str, case_id: str) -> Optional[Dict[str, Any]]:
    init_db(db_path)
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
        return dict(row) if row else None


def update_pattern(db_path: str, anonymized_key: Optional[str], category: str) -> int:
    if not anonymized_key:
        return 0
    init_db(db_path)
    now = utc_now()
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM offender_patterns WHERE anonymized_suspect_key = ?", (anonymized_key,)).fetchone()
        if row:
            cats = json.loads(row["categories_json"] or "{}")
            cats[category] = cats.get(category, 0) + 1
            count = int(row["case_count"]) + 1
            conn.execute(
                "UPDATE offender_patterns SET last_seen=?, case_count=?, categories_json=? WHERE anonymized_suspect_key=?",
                (now, count, json.dumps(cats), anonymized_key),
            )
            return count
        cats = {category: 1}
        conn.execute(
            "INSERT INTO offender_patterns VALUES (?, ?, ?, ?, ?)",
            (anonymized_key, now, now, 1, json.dumps(cats)),
        )
        return 1


def insert_feedback(db_path: str, row: Dict[str, Any]) -> None:
    init_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO feedback VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                row["feedback_id"], row["case_id"], row.get("reviewer_alias", "reviewer"),
                row.get("rating"), 1 if row.get("useful") else 0, row.get("notes"), row["timestamp_utc"],
            ),
        )


def audit(db_path: str, event_type: str, case_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
    import uuid
    init_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            "INSERT INTO audit_events VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), event_type, case_id, utc_now(), json.dumps(details or {}, ensure_ascii=False)),
        )


def summary(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    init_db(db_path)
    with connect(db_path) as conn:
        case_count = conn.execute("SELECT COUNT(*) AS c FROM cases").fetchone()["c"]
        evidence_count = conn.execute("SELECT COUNT(*) AS c FROM evidence").fetchone()["c"]
        feedback_count = conn.execute("SELECT COUNT(*) AS c FROM feedback").fetchone()["c"]
        categories = [dict(r) for r in conn.execute("SELECT category, COUNT(*) AS count FROM cases GROUP BY category ORDER BY count DESC")]
        priorities = [dict(r) for r in conn.execute("SELECT priority, COUNT(*) AS count FROM cases GROUP BY priority ORDER BY count DESC")]
        high_patterns = [dict(r) for r in conn.execute("SELECT anonymized_suspect_key, case_count, categories_json FROM offender_patterns WHERE case_count > 1 ORDER BY case_count DESC LIMIT 10")]
    return {
        "case_count": case_count,
        "evidence_count": evidence_count,
        "feedback_count": feedback_count,
        "categories": categories,
        "priorities": priorities,
        "repeat_patterns": high_patterns,
    }
