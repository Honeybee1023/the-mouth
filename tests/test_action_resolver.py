import json
from types import SimpleNamespace

import pytest

from mouth.models import PrimitiveAction
from mouth.providers import claude as claude_module


class FakeMessages:
    def __init__(self, response_text: str):
        self.response_text = response_text
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text=self.response_text)])


class FakeAnthropic:
    def __init__(self, api_key: str, response_text: str):
        self.api_key = api_key
        self.messages = FakeMessages(response_text=response_text)


def test_resolve_actions_parses_coordinates(monkeypatch):
    payload = [
        {
            "action_type": "mouse_move",
            "coordinates": [10, 20],
            "drag_to": None,
            "text": None,
            "keys": None,
            "confidence": 0.9,
            "source_primitive_idx": 0,
        }
    ]
    fake = FakeAnthropic(api_key="test", response_text=json.dumps(payload))
    monkeypatch.setattr(claude_module, "Anthropic", lambda api_key: fake)

    provider = claude_module.ClaudeProvider(api_key="test")
    primitive = PrimitiveAction(
        action_type="set_property",
        target="title",
        parameters={"property": "font_size", "value": 18},
        ordering=1,
    )
    result = provider.resolve_actions(primitive, screenshot_b64="abc123", app_context=None)

    assert result[0].coordinates == (10, 20)
    assert result[0].confidence == 0.9


def test_resolve_actions_sends_image_block(monkeypatch):
    fake = FakeAnthropic(api_key="test", response_text="[]")
    monkeypatch.setattr(claude_module, "Anthropic", lambda api_key: fake)

    provider = claude_module.ClaudeProvider(api_key="test")
    primitive = PrimitiveAction(
        action_type="open_menu",
        target="format",
        parameters={},
        ordering=1,
    )
    provider.resolve_actions(primitive, screenshot_b64="abc123", app_context="slides")

    message = fake.messages.last_kwargs["messages"][0]
    assert message["role"] == "user"
    content = message["content"]
    assert content[0]["type"] == "image"
    assert content[0]["source"]["data"] == "abc123"


def test_resolve_actions_raises_on_invalid_json(monkeypatch):
    fake = FakeAnthropic(api_key="test", response_text="not json")
    monkeypatch.setattr(claude_module, "Anthropic", lambda api_key: fake)

    provider = claude_module.ClaudeProvider(api_key="test")
    primitive = PrimitiveAction(
        action_type="open_menu",
        target="format",
        parameters={},
        ordering=1,
    )
    with pytest.raises(ValueError, match="invalid JSON"):
        provider.resolve_actions(primitive, screenshot_b64="abc123", app_context=None)
