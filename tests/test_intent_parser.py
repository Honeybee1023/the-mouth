import json
from types import SimpleNamespace

import pytest

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


def test_parse_intent_prompt_construction(monkeypatch):
    response_text = "[]"
    fake = FakeAnthropic(api_key="test", response_text=response_text)

    def fake_anthropic(api_key: str):
        assert api_key == "test"
        return fake

    monkeypatch.setattr(claude_module, "Anthropic", fake_anthropic)

    provider = claude_module.ClaudeProvider(api_key="test")
    provider.parse_intent("Hello", app_context="slides", primitives_schema=None)

    loaded_prompt = claude_module._load_prompt("intent_system.txt")
    assert fake.messages.last_kwargs["system"] == loaded_prompt
    assert fake.messages.last_kwargs["model"] == "claude-sonnet-4-20250514"


def test_parse_intent_parses_valid_json(monkeypatch):
    payload = [
        {
            "action_type": "set_property",
            "target": "title",
            "parameters": {"property": "font_size", "value": 18},
            "ordering": 1,
            "depends_on": None,
        }
    ]
    response_text = json.dumps(payload)
    fake = FakeAnthropic(api_key="test", response_text=response_text)

    monkeypatch.setattr(claude_module, "Anthropic", lambda api_key: fake)

    provider = claude_module.ClaudeProvider(api_key="test")
    result = provider.parse_intent("Make title bigger", app_context=None, primitives_schema=None)

    assert result[0].target == "title"
    assert result[0].parameters["value"] == 18


def test_parse_intent_raises_on_invalid_json(monkeypatch):
    fake = FakeAnthropic(api_key="test", response_text="not json")
    monkeypatch.setattr(claude_module, "Anthropic", lambda api_key: fake)

    provider = claude_module.ClaudeProvider(api_key="test")
    with pytest.raises(ValueError, match="invalid JSON"):
        provider.parse_intent("Bad", app_context=None, primitives_schema=None)
