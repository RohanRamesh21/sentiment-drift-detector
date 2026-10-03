from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class CollectorState:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS processed_submissions (id TEXT PRIMARY KEY, processed_at TEXT NOT NULL)")
            conn.execute("CREATE TABLE IF NOT EXISTS processed_comments (id TEXT PRIMARY KEY, processed_at TEXT NOT NULL)")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS collector_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_type TEXT NOT NULL,
                    subreddit TEXT NOT NULL,
                    items_seen INTEGER NOT NULL,
                    items_new INTEGER NOT NULL,
                    items_skipped INTEGER NOT NULL,
                    output_path TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

    def get_processed_ids(self, kind: str) -> set[str]:
        table = self._table_for_kind(kind)
        with self._conn() as conn:
            rows = conn.execute(f"SELECT id FROM {table}").fetchall()
        return {row[0] for row in rows}

    def mark_processed_ids(self, kind: str, ids: list[str]) -> None:
        if not ids:
            return
        table = self._table_for_kind(kind)
        now = datetime.now(timezone.utc).isoformat()
        with self._conn() as conn:
            conn.executemany(
                f"INSERT OR IGNORE INTO {table} (id, processed_at) VALUES (?, ?)",
                [(rid, now) for rid in ids],
            )

    def record_run(
        self,
        run_type: str,
        subreddit: str,
        items_seen: int,
        items_new: int,
        items_skipped: int,
        output_path: str | None,
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO collector_runs (
                    run_type, subreddit, items_seen, items_new, items_skipped, output_path, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_type,
                    subreddit,
                    items_seen,
                    items_new,
                    items_skipped,
                    output_path,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

    @staticmethod
    def _table_for_kind(kind: str) -> str:
        if kind == "submission":
            return "processed_submissions"
        if kind == "comment":
            return "processed_comments"
        raise ValueError(f"Unsupported kind: {kind}")
