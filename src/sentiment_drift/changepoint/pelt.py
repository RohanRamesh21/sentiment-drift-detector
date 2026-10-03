from __future__ import annotations

import pandas as pd
import ruptures as rpt


def detect_changepoints(series: pd.DataFrame, pen: float = 5.0, value_col: str = "aggregate_sentiment") -> pd.DataFrame:
    if series.empty or len(series) < 3:
        return pd.DataFrame(
            columns=[
                "changepoint_timestamp",
                "pre_change_mean",
                "post_change_mean",
                "change_magnitude",
                "window_message_count",
            ]
        )

    df = series.copy().sort_values("timestamp").reset_index(drop=True)
    signal = df[[value_col]].to_numpy()

    model = rpt.Pelt(model="l2").fit(signal)
    points = model.predict(pen=pen)

    changes = []
    prev = 0
    for point in points[:-1]:
        pre = df.iloc[:point][value_col]
        post = df.iloc[point:][value_col]
        changes.append(
            {
                "changepoint_timestamp": df.iloc[point]["timestamp"],
                "pre_change_mean": float(pre.mean()) if not pre.empty else float("nan"),
                "post_change_mean": float(post.mean()) if not post.empty else float("nan"),
                "change_magnitude": float(post.mean() - pre.mean()) if (not pre.empty and not post.empty) else float("nan"),
                "window_message_count": int(df.iloc[prev:point].get("message_count", pd.Series(dtype=int)).sum()),
            }
        )
        prev = point

    return pd.DataFrame(changes)
