from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from cybershield_ai.core.models import RetrievedGuidance

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:  # pragma: no cover
    TfidfVectorizer = None
    cosine_similarity = None


@dataclass
class Section:
    title: str
    content: str


class LegalRAGEngine:
    """Small local retrieval engine for demo legal/support guidance.

    This is a RAG-style component. It retrieves relevant guidance from a local markdown file.
    It does not provide legal advice.
    """

    def __init__(self, knowledge_path: str = "data/demo/legal_knowledge.md"):
        self.knowledge_path = Path(knowledge_path)
        self.sections = self._load_sections()
        self.vectorizer = None
        self.matrix = None
        if TfidfVectorizer and self.sections:
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.matrix = self.vectorizer.fit_transform([s.title + " " + s.content for s in self.sections])

    def _load_sections(self) -> List[Section]:
        if not self.knowledge_path.exists():
            return []
        text = self.knowledge_path.read_text(encoding="utf-8")
        chunks = []
        current_title = "Introduction"
        current_lines = []
        for line in text.splitlines():
            if line.startswith("## "):
                if current_lines:
                    chunks.append(Section(current_title, "\n".join(current_lines).strip()))
                current_title = line.replace("##", "", 1).strip()
                current_lines = []
            elif line.strip() and not line.startswith("# "):
                current_lines.append(line)
        if current_lines:
            chunks.append(Section(current_title, "\n".join(current_lines).strip()))
        return chunks

    def retrieve(self, query: str, k: int = 3) -> List[RetrievedGuidance]:
        if not self.sections:
            return []
        if self.vectorizer is None or self.matrix is None:
            return self._keyword_retrieve(query, k)
        qv = self.vectorizer.transform([query])
        scores = cosine_similarity(qv, self.matrix).ravel()
        order = scores.argsort()[::-1][:k]
        return [
            RetrievedGuidance(title=self.sections[i].title, content=self.sections[i].content, score=round(float(scores[i]), 4))
            for i in order
            if scores[i] > 0
        ] or self._keyword_retrieve(query, k)

    def _keyword_retrieve(self, query: str, k: int) -> List[RetrievedGuidance]:
        words = set(query.lower().split())
        ranked = []
        for s in self.sections:
            content_words = set((s.title + " " + s.content).lower().split())
            score = len(words & content_words) / max(1, len(words))
            ranked.append((score, s))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [RetrievedGuidance(title=s.title, content=s.content, score=round(score, 4)) for score, s in ranked[:k]]
