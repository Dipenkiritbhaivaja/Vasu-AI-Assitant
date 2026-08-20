from __future__ import annotations

from assistant.nlp.commands import (
    COMMAND_SYNONYMS,
    PRESERVE_PAYLOAD_COMMANDS,
)
from assistant.nlp.normalizer import (
    Normalizer,
)
from assistant.nlp.phrase_normalizer import (
    PhraseNormalizer,
)


class NLPProcessor:

    def __init__(
        self,
    ) -> None:

        self._normalizer = Normalizer()
        self._phrase_normalizer = (
    PhraseNormalizer()
)

    def process(
        self,
        text: str,
    ) -> str:

        text = self._phrase_normalizer.normalize(
            text,
        )

        words = text.split()

        if not words:
            return text

        for index, word in enumerate(words):

            normalized = COMMAND_SYNONYMS.get(
                word.lower(),
            )

            if normalized is None:
                continue

            payload = " ".join(
                words[index + 1 :]
            )

            if (
                normalized
                in PRESERVE_PAYLOAD_COMMANDS
            ):
                if payload:
                    return (
                        f"{normalized} {payload}"
                    )

                return normalized

            remaining = " ".join(
                words[index + 1 :]
            )

            if remaining:
                return (
                    f"{normalized} "
                    f"{remaining}"
                )

            return normalized

        return self._normalizer.normalize(
            text,
        )