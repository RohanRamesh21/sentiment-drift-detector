import pytest

from sentiment_drift.config import ConfigError, load_settings


def test_load_settings_missing(monkeypatch):
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    with pytest.raises(ConfigError):
        load_settings()
