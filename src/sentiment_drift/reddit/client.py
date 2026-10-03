from __future__ import annotations

import praw

from sentiment_drift.config import Settings, load_settings


class RedditClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or load_settings()
        self._client = praw.Reddit(
            client_id=self._settings.reddit_client_id,
            client_secret=self._settings.reddit_client_secret,
            user_agent=self._settings.reddit_user_agent,
            check_for_async=False,
        )
        self._client.read_only = True

    @property
    def client(self) -> praw.Reddit:
        return self._client

    def subreddit(self, name: str):
        return self._client.subreddit(name)

    def test_connection(self, subreddit_name: str = "stocks", limit: int = 3) -> int:
        submissions = list(self.subreddit(subreddit_name).new(limit=limit))
        return len(submissions)
