"""
NLP Processor.
"""

from __future__ import annotations

from assistant.nlp.normalizer import Normalizer


class NLPProcessor:

    def __init__(
        self,
    ) -> None:

        self._normalizer = Normalizer()

    def process(
        self,
        text: str,
    ) -> str:

        return self._normalizer.normalize(
            text,
        )