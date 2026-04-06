from mouth.models import ExecutionAction, MouthInput, MouthOutput, PrimitiveAction


def test_mouth_input_defaults():
    payload = MouthInput(user_utterance="Create a title")
    assert payload.user_utterance == "Create a title"
    assert payload.app_context is None
    assert payload.metadata == {}


def test_primitive_action_instantiation():
    action = PrimitiveAction(
        action_type="create_element",
        target="title",
        parameters={"kind": "textbox"},
        ordering=1,
        depends_on=None,
    )
    assert action.action_type == "create_element"
    assert action.target == "title"
    assert action.parameters["kind"] == "textbox"


def test_primitive_action_without_target():
    action = PrimitiveAction(
        action_type="select_all_text",
        parameters={},
        ordering=1,
    )
    assert action.target is None


def test_execution_action_instantiation():
    action = ExecutionAction(
        action_type="mouse_click",
        coordinates=(120, 240),
        source_primitive_idx=0,
    )
    assert action.action_type == "mouse_click"
    assert action.coordinates == (120, 240)
    assert action.source_primitive_idx == 0


def test_mouth_output_instantiation():
    primitive = PrimitiveAction(
        action_type="set_property",
        target="title",
        parameters={"property": "font_size", "value": 18},
        ordering=1,
    )
    output = MouthOutput(primitives=[primitive], actions=None)
    assert output.primitives[0].target == "title"
    assert output.actions is None
