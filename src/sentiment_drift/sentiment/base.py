from __future__ import annotations

from abc import ABC, abstractmethod


class SentimentModel(ABC):
    @abstractmethod
    def predict(self, texts: list[str]) -> list[dict]:
        raise NotImplementedError
