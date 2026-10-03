from __future__ import annotations

from datetime import datetime, timezone

from sentiment_drift.sentiment.base import SentimentModel


class TransformerSentimentModel(SentimentModel):
    def __init__(
        self,
        model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest",
        model_version: str = "latest",
    ) -> None:
        try:
            from transformers import pipeline
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("transformers is required. Install with `pip install -e .[ml]`") from exc

        self.model_name = model_name
        self.model_version = model_version
        self._pipeline = pipeline("sentiment-analysis", model=model_name, top_k=None)

    def predict(self, texts: list[str]) -> list[dict]:
        raw = self._pipeline(texts)
        now = datetime.now(timezone.utc).isoformat()
        output: list[dict] = []
        for entry in raw:
            probs = {item["label"].lower(): float(item["score"]) for item in entry}
            negative = probs.get("negative", probs.get("label_0", 0.0))
            neutral = probs.get("neutral", probs.get("label_1", 0.0))
            positive = probs.get("positive", probs.get("label_2", 0.0))
            output.append(
                {
                    "negative_probability": negative,
                    "neutral_probability": neutral,
                    "positive_probability": positive,
                    "sentiment_score": positive - negative,
                    "model_name": self.model_name,
                    "model_version": self.model_version,
                    "inference_timestamp": now,
                }
            )
        return output
