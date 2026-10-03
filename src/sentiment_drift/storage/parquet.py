from __future__ import annotations

from datetime import timezone
from pathlib import Path

import pandas as pd


def write_partitioned_records(records: list[dict], base_dir: Path, kind: str) -> str | None:
    if not records:
        return None

    df = pd.DataFrame(records)
    df["created_utc"] = pd.to_datetime(df["created_utc"], utc=True)
    df["date"] = df["created_utc"].dt.tz_convert(timezone.utc).dt.date.astype(str)

    output_path = None
    for date, group in df.groupby("date"):
        out_dir = base_dir / "raw" / f"{kind}s" / f"date={date}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"batch-{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}.parquet"
        group.drop(columns=["date"]).to_parquet(out_file, index=False)
        output_path = str(out_file)

    return output_path
