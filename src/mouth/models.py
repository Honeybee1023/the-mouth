from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MouthInput(BaseModel):
    user_utterance: str
    app_context: str | None = None
    metadata: dict = Field(default_factory=dict)


class PrimitiveAction(BaseModel):
    action_type: str
    target: str | None = None
    parameters: dict
    ordering: int
    depends_on: list[int] | None = None


class ExecutionAction(BaseModel):
    action_type: Literal[
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_drag",
        "keyboard_type",
        "keyboard_shortcut",
        "scroll",
        "wait",
    ]
    coordinates: tuple[int, int] | None = None
    drag_to: tuple[int, int] | None = None
    text: str | None = None
    keys: list[str] | None = None
    confidence: float = 0.0
    source_primitive_idx: int


class MouthOutput(BaseModel):
    primitives: list[PrimitiveAction]
    actions: list[ExecutionAction] | None = None
