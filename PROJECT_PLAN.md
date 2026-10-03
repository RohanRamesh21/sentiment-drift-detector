# Project Plan

This repository implements the phased plan for a sentiment drift detector over Reddit finance communities.

## MVP milestones

1. Repository bootstrap and package structure.
2. Official Reddit API client via OAuth/PRAW.
3. Incremental submissions + comments ingestion.
4. Deduplication and SQLite collector state.
5. Incremental Parquet storage.
6. Deterministic normalization.
7. Pluggable pretrained sentiment inference.
8. Time-series aggregation (15m/1h/1d).
9. PELT changepoint detection (`ruptures`).
10. Event correlation with configurable windows.

## Principles

- API compliance (official Reddit Data API only).
- No secrets in Git.
- Restart-safe collector operation.
- Batch/polling architecture first; no streaming infra for MVP.
