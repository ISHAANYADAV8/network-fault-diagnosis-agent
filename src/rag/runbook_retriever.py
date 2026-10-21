"""
Runbook Retriever Module (RAG)
Indexes domain troubleshooting runbooks and retrieves relevant diagnostic
procedures based on symptoms and error outputs.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class RunbookRetriever:
    def __init__(self, runbooks_dir: Optional[str | Path] = None):
        if runbooks_dir is None:
            runbooks_dir = Path(__file__).resolve().parent.parent.parent / "data" / "runbooks"
        self.runbooks_dir = Path(runbooks_dir)
        self.documents: List[Dict[str, str]] = []
        self._load_runbooks()

    def _tokenize(self, text: str) -> List[str]:
        """Simple alphanumeric tokenizer in lowercase."""
        return re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())

    def _load_runbooks(self) -> None:
        """Reads all markdown runbooks and splits them into distinct sections."""
        self.documents.clear()
        if not self.runbooks_dir.exists():
            return

        for filepath in self.runbooks_dir.glob("*.md"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Split into major sections
            sections = re.split(r"\n(?=##\s+)", content)
            title = sections[0].strip().replace("# ", "")
            for sec in sections:
                sec_text = sec.strip()
                if not sec_text:
                    continue
                tokens = self._tokenize(sec_text)
                self.documents.append({
                    "source": filepath.name,
                    "title": title,
                    "content": sec_text,
                    "tokens": tokens
                })

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        """
        Retrieves top_k most relevant runbook passages using BM25-style keyword relevance scoring.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.documents:
            return []

        scored_docs = []
        num_docs = len(self.documents)
        avg_doc_len = sum(len(d["tokens"]) for d in self.documents) / max(1, num_docs)

        for doc in self.documents:
            doc_tokens = doc["tokens"]
            doc_len = len(doc_tokens)
            score = 0.0

            for q_tok in set(query_tokens):
                # Term frequency in document
                tf = doc_tokens.count(q_tok)
                if tf == 0:
                    continue

                # Document frequency (number of docs containing token)
                df = sum(1 for d in self.documents if q_tok in d["tokens"])
                idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)

                # BM25 formula components (k1=1.5, b=0.75)
                k1 = 1.5
                b = 0.75
                denom = tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len))
                score += idf * ((tf * (k1 + 1.0)) / denom)

            if score > 0:
                scored_docs.append((score, doc))

        # Sort descending by score
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_docs[:top_k]]
