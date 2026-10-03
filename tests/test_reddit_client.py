import os

import pytest

from sentiment_drift.reddit.client import RedditClient


@pytest.mark.integration
def test_reddit_connection_live():
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]
    if any(not os.getenv(name) for name in required):
        pytest.skip("Reddit credentials are not configured in environment")

    count = RedditClient().test_connection(subreddit_name="stocks", limit=2)
    assert count >= 1
