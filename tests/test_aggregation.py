import pandas as pd

from sentiment_drift.aggregation.time_series import aggregate_sentiment


def test_aggregate_sentiment_outputs_expected_columns():
    df = pd.DataFrame(
        {
            "created_utc": [
                "2026-01-01T00:00:00Z",
                "2026-01-01T00:10:00Z",
                "2026-01-01T01:05:00Z",
            ],
            "sentiment_score": [0.8, -0.2, 0.4],
            "score": [10, 1, 3],
        }
    )

    out = aggregate_sentiment(df, freq="1H")

    assert list(out.columns) == [
        "timestamp",
        "mean_sentiment",
        "median_sentiment",
        "message_count",
        "positive_fraction",
        "negative_fraction",
        "engagement_weighted_sentiment",
    ]
    assert len(out) == 2
    assert out["message_count"].sum() == 3
