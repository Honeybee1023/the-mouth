from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ExecutionAction, PrimitiveAction


class Provider(ABC):
    @abstractmethod
    def parse_intent(
        self,
        utterance: str,
        app_context: str | None,
        primitives_schema: dict | None,
    ) -> list[PrimitiveAction]:
        raise NotImplementedError

    @abstractmethod
    def resolve_actions(
        self,
        primitive: PrimitiveAction,
        screenshot_b64: str,
        app_context: str | None,
    ) -> list[ExecutionAction]:
        raise NotImplementedError
