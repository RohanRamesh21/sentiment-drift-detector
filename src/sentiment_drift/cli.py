from __future__ import annotations

import argparse
import json

from sentiment_drift.config import load_settings
from sentiment_drift.ingestion.collector import Collector


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentiment-drift")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_sub = subparsers.add_parser("collect-submissions")
    collect_sub.add_argument("--subreddit", required=True)
    collect_sub.add_argument("--limit", type=int, default=100)

    collect_comments = subparsers.add_parser("collect-comments")
    collect_comments.add_argument("--subreddit", required=True)
    collect_comments.add_argument("--limit", type=int, default=25)
    collect_comments.add_argument("--comment-limit", type=int, default=200)

    conn_test = subparsers.add_parser("test-reddit-connection")
    conn_test.add_argument("--subreddit", default="stocks")
    conn_test.add_argument("--limit", type=int, default=3)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = load_settings()
    collector = Collector(settings)

    if args.command == "collect-submissions":
        result = collector.collect_submissions(subreddit=args.subreddit, limit=args.limit)
    elif args.command == "collect-comments":
        result = collector.collect_comments(
            subreddit=args.subreddit,
            limit=args.limit,
            comment_limit=args.comment_limit,
        )
    else:
        count = collector.reddit.test_connection(subreddit_name=args.subreddit, limit=args.limit)
        result = {"subreddit": args.subreddit, "items_retrieved": count}

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
