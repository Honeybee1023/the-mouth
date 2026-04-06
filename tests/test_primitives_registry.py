from mouth.primitives_registry import GOOGLE_SLIDES_PRIMITIVES, is_ungrounded


def test_registry_has_minimum_primitives():
    assert len(GOOGLE_SLIDES_PRIMITIVES) >= 15


def test_ungrounded_primitives_have_shortcuts():
    for action_type, spec in GOOGLE_SLIDES_PRIMITIVES.items():
        if is_ungrounded(action_type) and action_type != "type_text":
            assert spec.keyboard_shortcut


def test_is_ungrounded_true_for_bold():
    assert is_ungrounded("set_font_bold") is True


def test_is_ungrounded_false_for_select_element():
    assert is_ungrounded("select_element") is False
