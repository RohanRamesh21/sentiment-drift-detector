from __future__ import annotations

import re
import unicodedata


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str | None) -> str:
    if text is None:
        return ""
    normalized = unicodedata.normalize("NFKC", str(text))
    normalized = _WHITESPACE_RE.sub(" ", normalized).strip()
    return normalized


def normalize_record_text(record: dict, field: str = "body", output_field: str = "normalized_text") -> dict:
    updated = dict(record)
    updated[output_field] = normalize_text(record.get(field))
    return updated
