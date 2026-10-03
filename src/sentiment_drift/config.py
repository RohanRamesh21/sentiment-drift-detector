from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    data_dir: Path = Path("data")
    state_db_path: Path = Path("data/state/collector_state.sqlite")
    retention_days: int = 30


class ConfigError(ValueError):
    """Configuration validation failure."""


def load_settings() -> Settings:
    load_dotenv()

    client_id = os.getenv("REDDIT_CLIENT_ID", "").strip()
    client_secret = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
    user_agent = os.getenv("REDDIT_USER_AGENT", "").strip()

    missing = []
    if not client_id:
        missing.append("REDDIT_CLIENT_ID")
    if not client_secret:
        missing.append("REDDIT_CLIENT_SECRET")
    if not user_agent:
        missing.append("REDDIT_USER_AGENT")

    if missing:
        raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")

    if "sentiment-drift" not in user_agent and "by u/" not in user_agent:
        raise ConfigError(
            "REDDIT_USER_AGENT should be descriptive, e.g. sentiment-drift-detector/0.1 (by u/your_username)"
        )

    return Settings(
        reddit_client_id=client_id,
        reddit_client_secret=client_secret,
        reddit_user_agent=user_agent,
    )
