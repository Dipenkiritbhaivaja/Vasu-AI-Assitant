from __future__ import annotations

from assistant.nlp.phrases import PHRASES


class PhraseNormalizer:

    def normalize(
        self,
        text: str,
    ) -> str:

        normalized = text.lower()

        for phrase, replacement in PHRASES.items():
            normalized = normalized.replace(
                phrase,
                replacement,
            )

        return normalized