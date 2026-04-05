from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from ..models import ExecutionAction, PrimitiveAction
from .base import Provider


class ClaudeProvider(Provider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514") -> None:
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def parse_intent(
        self,
        utterance: str,
        app_context: str | None,
        primitives_schema: dict | None,
    ) -> list[PrimitiveAction]:
        system_prompt = _load_prompt("intent_system.txt")
        user_payload = {
            "utterance": utterance,
            "app_context": app_context,
            "primitives_schema": primitives_schema,
        }
        response = self._client.messages.create(
            model=self._model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=True),
                }
            ],
        )
        text = _extract_text(response)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Claude returned invalid JSON for intent parsing") from exc

        if not isinstance(data, list):
            raise ValueError("Claude intent response must be a JSON array")

        return [PrimitiveAction.model_validate(item) for item in data]

    def resolve_actions(
        self,
        primitive: PrimitiveAction,
        screenshot_b64: str,
        app_context: str | None,
    ) -> list[ExecutionAction]:
        system_prompt = _load_prompt("resolve_system.txt")
        user_payload = {
            "primitive": primitive.model_dump(),
            "app_context": app_context,
        }
        response = self._client.messages.create(
            model=self._model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": screenshot_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": json.dumps(user_payload, ensure_ascii=True),
                        },
                    ],
                }
            ],
        )
        text = _extract_text(response)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(\"Claude returned invalid JSON for action resolving\") from exc

        if not isinstance(data, list):
            raise ValueError(\"Claude action response must be a JSON array\")

        return [ExecutionAction.model_validate(item) for item in data]


def _load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8")


def _extract_text(response: Any) -> str:
    content = getattr(response, "content", None)
    if not content:
        raise ValueError("Claude returned empty response content")

    first = content[0]
    text = getattr(first, "text", None)
    if not text:
        raise ValueError("Claude response did not include text output")
    return text
