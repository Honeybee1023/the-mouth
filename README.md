# agent-one-mouth

**the-mouth** is the neural translation engine for Agent One, a neuro-symbolic Programming by Demonstration platform built at MIT CSAIL. It decomposes freeform natural language instructions into structured UI primitives using LLM reasoning, then grounds those primitives to pixel-precise mouse and keyboard actions using VLM visual understanding — bridging the gap between what a user *says* and what a browser *does*.

**Three layers**
1. Natural language intent
2. Primitive actions (platform-agnostic)
3. Execution actions (mouse/keyboard)

**Installation**
```bash
pip install -e .
```

**Usage: full pipeline (single screenshot)**
```python
from mouth import Mouth

mouth = Mouth(provider="claude", api_key="...")
result = mouth.process(
    utterance="Make a title for this slide, red font, size 18",
    screenshot=screenshot_bytes,
    app_context="google_slides",
)

print(result.primitives)
print(result.actions)
```

**Usage: iterative per-primitive (recommended)**
```python
from mouth import Mouth

mouth = Mouth(provider="claude", api_key="...")
primitives = mouth.parse_intent(
    utterance="Make a title for this slide, red font, size 18",
    app_context="google_slides",
)

for primitive in primitives:
    screenshot = nodriver.capture()  # external screen capture
    actions = mouth.resolve_actions(
        primitive=primitive,
        screenshot=screenshot,
        app_context="google_slides",
    )
    for action in actions:
        nodriver.execute(action)     # external execution
```

**Notes**
- The `process()` convenience method resolves all primitives against the same screenshot.
- For production use, prefer the per-primitive loop with fresh screenshots.
