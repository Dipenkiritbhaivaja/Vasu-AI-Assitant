"""
Text normalization.
"""

from __future__ import annotations

import string

from assistant.nlp.stopwords import STOPWORDS


class Normalizer:

    def normalize(
        self,
        text: str,
    ) -> str:

        text = text.lower()

        punctuation = string.punctuation

        words = []

        for word in text.split():

            word = word.strip(
                punctuation,
            )

            if not word:
                continue

            if word in STOPWORDS:
                continue

            words.append(
                word,
            )

        return " ".join(
            words,
        )