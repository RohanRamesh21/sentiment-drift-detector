from __future__ import annotations

from pathlib import Path

from sentiment_drift.config import Settings
from sentiment_drift.ingestion.dedup import deduplicate_records
from sentiment_drift.ingestion.state import CollectorState
from sentiment_drift.reddit.client import RedditClient
from sentiment_drift.reddit.comments import normalize_comment
from sentiment_drift.reddit.submissions import normalize_submission
from sentiment_drift.storage.parquet import write_partitioned_records


class Collector:
    def __init__(self, settings: Settings, state: CollectorState | None = None) -> None:
        self.settings = settings
        self.reddit = RedditClient(settings)
        self.state = state or CollectorState(settings.state_db_path)

    def collect_submissions(self, subreddit: str, limit: int = 100) -> dict:
        raw_items = list(self.reddit.subreddit(subreddit).new(limit=limit))
        normalized = [normalize_submission(item, subreddit) for item in raw_items]
        existing = self.state.get_processed_ids("submission")
        new_records, skipped = deduplicate_records(normalized, existing)

        output = write_partitioned_records(new_records, self.settings.data_dir, kind="submission")
        self.state.mark_processed_ids("submission", [r["id"] for r in new_records])
        self.state.record_run("collect-submissions", subreddit, len(normalized), len(new_records), skipped, output)

        return {
            "subreddit": subreddit,
            "items_seen": len(normalized),
            "items_new": len(new_records),
            "items_skipped": skipped,
            "output_path": output,
        }

    def collect_comments(self, subreddit: str, limit: int = 25, comment_limit: int = 200) -> dict:
        submissions = list(self.reddit.subreddit(subreddit).new(limit=limit))
        comments: list[dict] = []

        for submission in submissions:
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list()[:comment_limit]:
                comments.append(normalize_comment(comment, subreddit, submission.id))

        existing = self.state.get_processed_ids("comment")
        new_records, skipped = deduplicate_records(comments, existing)

        output = write_partitioned_records(new_records, self.settings.data_dir, kind="comment")
        self.state.mark_processed_ids("comment", [r["id"] for r in new_records])
        self.state.record_run("collect-comments", subreddit, len(comments), len(new_records), skipped, output)

        return {
            "subreddit": subreddit,
            "items_seen": len(comments),
            "items_new": len(new_records),
            "items_skipped": skipped,
            "output_path": output,
        }
