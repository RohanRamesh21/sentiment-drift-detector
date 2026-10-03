from sentiment_drift.preprocessing.normalize import normalize_text


def test_normalize_text_preserves_sentiment_signal_tokens():
    text = "  Bullish   on $NVDA 🚀\n\n  still not bearish!!!  "
    normalized = normalize_text(text)
    assert normalized == "Bullish on $NVDA 🚀 still not bearish!!!"


def test_normalize_text_handles_none():
    assert normalize_text(None) == ""
