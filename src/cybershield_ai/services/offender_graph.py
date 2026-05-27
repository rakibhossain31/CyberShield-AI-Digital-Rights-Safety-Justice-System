from __future__ import annotations

from typing import Optional
from cybershield_ai.core.security import hash_identifier
from cybershield_ai.core import database


def anonymize_suspect(identifier: Optional[str]) -> Optional[str]:
    return hash_identifier(identifier)


def register_pattern(db_path: str, suspect_identifier: Optional[str], category: str) -> tuple[Optional[str], int]:
    key = anonymize_suspect(suspect_identifier)
    count = database.update_pattern(db_path, key, category) if key else 0
    return key, count
