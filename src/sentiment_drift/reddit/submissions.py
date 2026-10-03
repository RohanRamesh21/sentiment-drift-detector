from __future__ import annotations

from datetime import datetime, timezone


def normalize_submission(item, subreddit: str) -> dict:
    return {
        "id": item.id,
        "subreddit": subreddit,
        "type": "submission",
        "created_utc": datetime.fromtimestamp(item.created_utc, tz=timezone.utc),
        "title": getattr(item, "title", None),
        "body": getattr(item, "selftext", None),
        "score": int(getattr(item, "score", 0) or 0),
        "num_comments": int(getattr(item, "num_comments", 0) or 0),
        "permalink": getattr(item, "permalink", None),
        "url": getattr(item, "url", None),
        "submission_id": item.id,
        "retrieved_at": datetime.now(timezone.utc),
    }
