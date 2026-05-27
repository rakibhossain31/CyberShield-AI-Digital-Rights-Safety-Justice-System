from __future__ import annotations

import hashlib
import uuid
from cybershield_ai.core import database
from cybershield_ai.core.models import EvidenceRecord
from cybershield_ai.core.security import sha256_text


class EvidenceVault:
    def __init__(self, db_path: str = database.DEFAULT_DB_PATH):
        self.db_path = db_path
        database.init_db(db_path)

    def add_text_evidence(self, case_id: str, evidence_name: str, evidence_text: str, collector_alias: str = "demo_user") -> EvidenceRecord:
        evidence_hash = sha256_text(evidence_text)
        previous_chain_hash = database.last_chain_hash(self.db_path)
        timestamp = database.utc_now()
        chain_material = f"{previous_chain_hash}|{case_id}|{evidence_name}|{evidence_hash}|{timestamp}"
        chain_hash = hashlib.sha256(chain_material.encode("utf-8")).hexdigest()
        record = EvidenceRecord(
            evidence_id=str(uuid.uuid4()),
            case_id=case_id,
            evidence_name=evidence_name,
            evidence_hash=evidence_hash,
            chain_hash=chain_hash,
            timestamp_utc=timestamp,
            collector_alias=collector_alias,
        )
        database.insert_evidence(
            self.db_path,
            {
                **record.model_dump(),
                "previous_chain_hash": previous_chain_hash,
                "metadata": {"storage_mode": "hash_only_demo", "content_stored": False},
            },
        )
        database.audit(self.db_path, "evidence_hashed", case_id, {"evidence_id": record.evidence_id, "evidence_name": evidence_name})
        return record
