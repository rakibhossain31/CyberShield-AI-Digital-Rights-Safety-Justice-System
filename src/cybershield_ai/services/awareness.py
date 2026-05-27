from __future__ import annotations

import json
from pathlib import Path
from typing import List

DEFAULT_TIPS = ["Preserve evidence.", "Document the timeline.", "Seek trusted human support if harm escalates."]


class AwarenessEngine:
    def __init__(self, path: str = "data/demo/awareness_guidance.json"):
        self.path = Path(path)
        self.tips = self._load()

    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {"other": DEFAULT_TIPS}

    def tips_for(self, category: str) -> List[str]:
        return list(self.tips.get(category, self.tips.get("other", DEFAULT_TIPS)))
