# agent-one-mouth

The Mouth is a translation layer that converts natural language intent into low-level browser execution actions. It is designed to stay stateless and pure: it never executes actions or captures screens. It only translates.

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
