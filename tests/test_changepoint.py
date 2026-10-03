import numpy as np
import pandas as pd

from sentiment_drift.changepoint.pelt import detect_changepoints


def test_detect_changepoint_on_synthetic_signal():
    rng = np.random.default_rng(42)
    pre = rng.normal(0.1, 0.02, 500)
    post = rng.normal(-0.4, 0.02, 500)
    signal = np.concatenate([pre, post])

    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=len(signal), freq="min", tz="UTC"),
            "aggregate_sentiment": signal,
            "message_count": 1,
        }
    )

    cps = detect_changepoints(df, pen=10.0)

    assert not cps.empty
    minute = int((cps["changepoint_timestamp"].iloc[0] - df["timestamp"].iloc[0]).total_seconds() // 60)
    assert 450 <= minute <= 550
