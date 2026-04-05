from __future__ import annotations

from .models import ExecutionAction, PrimitiveAction
from .providers.base import Provider


def resolve_actions(
    primitive: PrimitiveAction,
    screenshot_b64: str,
    app_context: str | None,
    provider: Provider,
) -> list[ExecutionAction]:
    return provider.resolve_actions(
        primitive=primitive,
        screenshot_b64=screenshot_b64,
        app_context=app_context,
    )
