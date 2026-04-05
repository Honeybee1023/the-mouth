from mouth.models import ExecutionAction, PrimitiveAction
from mouth.mouth import Mouth


class FakeProvider:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def parse_intent(self, utterance, app_context, primitives_schema):
        return [
            PrimitiveAction(
                action_type="set_property",
                target="title",
                parameters={"property": "font_size", "value": 18},
                ordering=1,
            )
        ]

    def resolve_actions(self, primitive, screenshot_b64, app_context):
        return [
            ExecutionAction(
                action_type="mouse_click",
                coordinates=(1, 2),
                source_primitive_idx=0,
            )
        ]


def test_process_runs_full_pipeline(monkeypatch):
    monkeypatch.setattr(Mouth, "_PROVIDERS", {"fake": FakeProvider})

    mouth = Mouth(provider="fake", api_key="unused")
    result = mouth.process(
        utterance="Make title bigger",
        screenshot=b"fakebytes",
        app_context="slides",
    )

    assert result.primitives[0].target == "title"
    assert result.actions[0].action_type == "mouse_click"
