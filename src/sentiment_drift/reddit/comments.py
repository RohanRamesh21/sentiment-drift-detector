from __future__ import annotations

from datetime import datetime, timezone


def normalize_comment(item, subreddit: str, submission_id: str) -> dict:
    return {
        "id": item.id,
        "subreddit": subreddit,
        "type": "comment",
        "created_utc": datetime.fromtimestamp(item.created_utc, tz=timezone.utc),
        "body": getattr(item, "body", None),
        "score": int(getattr(item, "score", 0) or 0),
        "parent_id": getattr(item, "parent_id", None),
        "submission_id": submission_id,
        "retrieved_at": datetime.now(timezone.utc),
    }
