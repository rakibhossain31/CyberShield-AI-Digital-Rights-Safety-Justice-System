from __future__ import annotations

import hashlib
import os
import re
from typing import Optional

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d[\d\s\-()]{7,}\d)")
URL_RE = re.compile(r"https?://\S+")


def redact_text(text: str) -> str:
    """Redact obvious emails, phone numbers, and URLs from free text."""
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = URL_RE.sub("[REDACTED_URL]", text)
    return text


def hash_identifier(identifier: Optional[str], salt: Optional[str] = None) -> Optional[str]:
    if not identifier:
        return None
    salt = salt or os.getenv("CYBERSHIELD_SALT", "change-this-demo-salt")
    normalized = identifier.strip().lower()
    digest = hashlib.sha256(f"{salt}:{normalized}".encode("utf-8")).hexdigest()
    return digest[:24]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
