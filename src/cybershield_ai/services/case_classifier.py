from __future__ import annotations

from typing import Dict, List
from cybershield_ai.core.models import ClassificationResult

KEYWORDS: Dict[str, List[str]] = {
    "blackmail": ["blackmail", "leak", "private photo", "demanding money", "extort", "intimate", "release", "pay"],
    "hacking": ["hacked", "unauthorized", "login", "password", "account access", "recovery", "otp", "2fa", "device"],
    "harassment": ["harass", "abusive", "threat", "repeated", "bully", "stalking", "message", "insult"],
    "impersonation": ["fake profile", "impersonat", "using my photo", "pretending", "copied my name"],
    "doxxing": ["address", "phone number", "personal information", "doxx", "posted my location", "workplace"],
    "financial_fraud": ["transaction", "wallet", "bank", "payment", "money", "fraud", "scam", "bkash", "nagad"],
}


def classify_case(statement: str) -> ClassificationResult:
    text = statement.lower()
    scores = {}
    matched = {}
    for category, terms in KEYWORDS.items():
        hits = [t for t in terms if t in text]
        if hits:
            scores[category] = len(hits)
            matched[category] = hits
    if not scores:
        return ClassificationResult(
            category="other",
            confidence=0.35,
            matched_terms=[],
            explanation="No strong keyword pattern was detected, so the report needs manual review.",
        )
    category = max(scores, key=scores.get)
    confidence = min(0.95, 0.45 + 0.12 * scores[category])
    return ClassificationResult(
        category=category,
        confidence=round(confidence, 2),
        matched_terms=matched[category],
        explanation=f"Detected {category} indicators from matched terms: {', '.join(matched[category])}.",
    )
