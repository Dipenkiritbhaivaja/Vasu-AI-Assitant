"""
Text normalization.
"""

from __future__ import annotations

import re
import string

from assistant.nlp.stopwords import STOPWORDS
from assistant.nlp.synonyms import SYNONYMS


class Normalizer:

    def normalize(
        self,
        text: str,
    ) -> str:

        text = text.lower()

        text = text.translate(
            str.maketrans(
                "",
                "",
                string.punctuation,
            )
        )

        words = []

        for word in text.split():

            if word in STOPWORDS:
                continue

            word = SYNONYMS.get(
                word,
                word,
            )

            words.append(word)

        return " ".join(words)