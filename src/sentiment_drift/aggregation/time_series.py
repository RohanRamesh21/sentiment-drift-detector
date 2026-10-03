from __future__ import annotations

import numpy as np
import pandas as pd


def aggregate_sentiment(
    frame: pd.DataFrame,
    freq: str = "1H",
    timestamp_col: str = "created_utc",
    sentiment_col: str = "sentiment_score",
    score_col: str = "score",
) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "mean_sentiment",
                "median_sentiment",
                "message_count",
                "positive_fraction",
                "negative_fraction",
                "engagement_weighted_sentiment",
            ]
        )

    df = frame.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)
    normalized_freq = str(freq).lower()
    df["timestamp"] = df[timestamp_col].dt.floor(normalized_freq)
    df["weight"] = np.log1p(np.clip(df.get(score_col, 0), 0, None))

    def weighted_mean(group: pd.DataFrame) -> float:
        weights = group["weight"].to_numpy()
        scores = group[sentiment_col].to_numpy()
        if np.allclose(weights.sum(), 0.0):
            return float(scores.mean())
        return float(np.average(scores, weights=weights))

    result = (
        df.groupby("timestamp", as_index=False)
        .apply(
            lambda g: pd.Series(
                {
                    "mean_sentiment": float(g[sentiment_col].mean()),
                    "median_sentiment": float(g[sentiment_col].median()),
                    "message_count": int(len(g)),
                    "positive_fraction": float((g[sentiment_col] > 0).mean()),
                    "negative_fraction": float((g[sentiment_col] < 0).mean()),
                    "engagement_weighted_sentiment": weighted_mean(g),
                }
            ),
            include_groups=False,
        )
        .reset_index(drop=True)
        .sort_values("timestamp")
    )
    return result
