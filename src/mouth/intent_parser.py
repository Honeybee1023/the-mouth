from __future__ import annotations

from .models import PrimitiveAction
from .providers.base import Provider


def parse_intent(
    utterance: str,
    app_context: str | None,
    provider: Provider,
    primitives_schema: dict | None = None,
) -> list[PrimitiveAction]:
    return provider.parse_intent(
        utterance=utterance,
        app_context=app_context,
        primitives_schema=primitives_schema,
    )
