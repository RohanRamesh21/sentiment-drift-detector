# Sentiment Drift Detector

A batch-first data engineering + ML project that tracks Reddit sentiment as a time series and identifies changepoints.

## Scope (MVP)

- Official Reddit Data API through OAuth + PRAW (no scraping).
- Incremental polling ingestion for configured finance subreddits.
- Local Parquet storage with deduplication by Reddit object ID.
- Deterministic text normalization.
- Pluggable sentiment model interface.
- Time-window aggregation and PELT changepoint detection.
- Basic event correlation.

## Setup

1. Copy `.env.example` to `.env` and set credentials:

```bash
cp .env.example .env
```

Required variables:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`

2. Install dependencies:

```bash
pip install -e .[dev]
```

Optional transformer inference:

```bash
pip install -e .[ml]
```

## CLI

Collect submissions:

```bash
python -m sentiment_drift.cli collect-submissions --subreddit wallstreetbets --limit 100
```

Collect comments:

```bash
python -m sentiment_drift.cli collect-comments --subreddit wallstreetbets --limit 25
```

## Data policy notes

- Do not commit `.env` or API credentials.
- Do not scrape Reddit HTML or use browser automation.
- Retention is configurable; data is not treated as permanent immutable archive.
- The MVP uses pretrained sentiment models only (no Reddit fine-tuning).
