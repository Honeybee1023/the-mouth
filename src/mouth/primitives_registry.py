"""Google Slides primitive action definitions.

Each primitive is categorized as grounded (needs VLM + screenshot),
ungrounded (pure keyboard), or hybrid (keyboard + one VLM grounding step).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GroundingType(Enum):
    UNGROUNDED = "ungrounded"  # pure keyboard, no VLM needed
    GROUNDED = "grounded"  # needs VLM + screenshot
    HYBRID = "hybrid"  # keyboard + one VLM grounding step


@dataclass(frozen=True)
class PrimitiveSpec:
    action_type: str
    grounding: GroundingType
    keyboard_shortcut: list[str] | None = None
    description: str = ""


GOOGLE_SLIDES_PRIMITIVES: dict[str, PrimitiveSpec] = {
    # --- Grounded (need VLM) ---
    "select_element": PrimitiveSpec(
        action_type="select_element",
        grounding=GroundingType.GROUNDED,
        description="Click on a specific element on the slide canvas.",
    ),
    "click_ui_control": PrimitiveSpec(
        action_type="click_ui_control",
        grounding=GroundingType.GROUNDED,
        description="Click a specific control in the toolbar or menus.",
    ),
    "insert_textbox": PrimitiveSpec(
        action_type="insert_textbox",
        grounding=GroundingType.GROUNDED,
        description="Insert a new text box on the slide.",
    ),
    # --- Ungrounded (pure keyboard) ---
    "select_all_text": PrimitiveSpec(
        action_type="select_all_text",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "a"],
        description="Select all text in the currently focused textbox.",
    ),
    "type_text": PrimitiveSpec(
        action_type="type_text",
        grounding=GroundingType.UNGROUNDED,
        description="Type a string of text.",
    ),
    "set_font_bold": PrimitiveSpec(
        action_type="set_font_bold",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "b"],
        description="Toggle bold formatting.",
    ),
    "set_font_italic": PrimitiveSpec(
        action_type="set_font_italic",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "i"],
        description="Toggle italic formatting.",
    ),
    "set_font_underline": PrimitiveSpec(
        action_type="set_font_underline",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "u"],
        description="Toggle underline formatting.",
    ),
    "undo": PrimitiveSpec(
        action_type="undo",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "z"],
        description="Undo last action.",
    ),
    "copy": PrimitiveSpec(
        action_type="copy",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "c"],
        description="Copy selection.",
    ),
    "paste": PrimitiveSpec(
        action_type="paste",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["ctrl", "v"],
        description="Paste clipboard.",
    ),
    "delete": PrimitiveSpec(
        action_type="delete",
        grounding=GroundingType.UNGROUNDED,
        keyboard_shortcut=["delete"],
        description="Delete selection.",
    ),
    # --- Hybrid (keyboard + one VLM grounding) ---
    "set_font_size": PrimitiveSpec(
        action_type="set_font_size",
        grounding=GroundingType.HYBRID,
        description="Change font size of selected text.",
    ),
    "set_font_color": PrimitiveSpec(
        action_type="set_font_color",
        grounding=GroundingType.HYBRID,
        description="Change font color of selected text.",
    ),
    "set_font_family": PrimitiveSpec(
        action_type="set_font_family",
        grounding=GroundingType.HYBRID,
        description="Change font of selected text.",
    ),
    "move_element": PrimitiveSpec(
        action_type="move_element",
        grounding=GroundingType.HYBRID,
        description="Move the selected element.",
    ),
}


def get_primitive_spec(action_type: str) -> PrimitiveSpec | None:
    return GOOGLE_SLIDES_PRIMITIVES.get(action_type)


def is_ungrounded(action_type: str) -> bool:
    spec = get_primitive_spec(action_type)
    return spec is not None and spec.grounding == GroundingType.UNGROUNDED
