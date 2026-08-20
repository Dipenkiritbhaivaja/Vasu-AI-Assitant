from __future__ import annotations

import re

from assistant.nlp.phrases import PHRASES


class PhraseNormalizer:

    def normalize(
        self,
        text: str,
    ) -> str:

        normalized = text

        for phrase, replacement in PHRASES.items():
            normalized = re.sub(
                re.escape(phrase),
                lambda _: replacement,
                normalized,
                flags=re.IGNORECASE,
            )

        return normalized