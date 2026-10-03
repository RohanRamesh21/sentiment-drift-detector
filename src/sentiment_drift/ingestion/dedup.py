from __future__ import annotations

from typing import Iterable


def deduplicate_records(records: Iterable[dict], existing_ids: set[str]) -> tuple[list[dict], int]:
    seen = set(existing_ids)
    output: list[dict] = []
    skipped = 0
    for record in records:
        rid = record["id"]
        if rid in seen:
            skipped += 1
            continue
        seen.add(rid)
        output.append(record)
    return output, skipped
