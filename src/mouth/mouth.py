from __future__ import annotations

import base64
from typing import Any

from .action_resolver import resolve_actions as resolve_actions_fn
from .intent_parser import parse_intent as parse_intent_fn
from .models import ExecutionAction, MouthOutput, PrimitiveAction
from .providers.base import Provider
from .providers.claude import ClaudeProvider


class Mouth:
    _PROVIDERS: dict[str, type[Provider]] = {
        "claude": ClaudeProvider,
    }

    def __init__(self, provider: str = "claude", **provider_kwargs: Any) -> None:
        if provider not in self._PROVIDERS:
            raise ValueError(f"Unknown provider '{provider}'")
        provider_cls = self._PROVIDERS[provider]
        self._provider = provider_cls(**provider_kwargs)

    def parse_intent(
        self,
        utterance: str,
        app_context: str | None = None,
        primitives_schema: dict | None = None,
    ) -> list[PrimitiveAction]:
        return parse_intent_fn(
            utterance=utterance,
            app_context=app_context,
            provider=self._provider,
            primitives_schema=primitives_schema,
        )

    def resolve_actions(
        self,
        primitive: PrimitiveAction,
        screenshot: bytes,
        app_context: str | None = None,
    ) -> list[ExecutionAction]:
        screenshot_b64 = base64.b64encode(screenshot).decode("ascii")
        return resolve_actions_fn(
            primitive=primitive,
            screenshot_b64=screenshot_b64,
            app_context=app_context,
            provider=self._provider,
        )

    def process(
        self,
        utterance: str,
        screenshot: bytes,
        app_context: str | None = None,
        primitives_schema: dict | None = None,
    ) -> MouthOutput:
        primitives = self.parse_intent(
            utterance=utterance,
            app_context=app_context,
            primitives_schema=primitives_schema,
        )
        actions: list[ExecutionAction] = []
        for primitive in primitives:
            actions.extend(
                self.resolve_actions(
                    primitive=primitive,
                    screenshot=screenshot,
                    app_context=app_context,
                )
            )
        return MouthOutput(primitives=primitives, actions=actions)
