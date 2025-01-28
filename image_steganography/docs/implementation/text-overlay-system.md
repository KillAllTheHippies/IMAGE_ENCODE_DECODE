# Text Overlay System Implementation Guide

## Security Implementation

### Input Validation

```python
class SafeTextValidator:
    """
    Enforces:
    - Max 4096 characters
    - Only printable Unicode
    - No control chars
    - Font whitelist
    """
    def sanitize(input_text: str, allowed_fonts: list) -> tuple[str, list]:
        ...
```

### Memory Limits

- Text buffers limited to 4MB RAM
- Layer cache uses LRU eviction (max 8 layers)
- File operations sandboxed to temp directory

## Theming Integration

### Font Configuration

```json
{
  "default_font": {
    "family": "Arial",
    "size": 12,
    "color": "#RRGGBBAA",
    "stroke": {
      "width": 1,
      "color": "#RRGGBB"
    }
  }
}
```

## Stored in ThemeManager.font_registry

## Coordinate System

```diagram

(0,0) Image Top-Left
  +-------------------+
  |                   |
  |                   |
  +-------------------+
                  (1,1) Image Bottom-Right

Position Calculation:
x_pixels = x_normalized * image_width
y_pixels = y_normalized * image_height
```

## Blend Modes (Porter-Duff Operators)

| Mode          | Formula                      |
|---------------|------------------------------|
| Over          | αₐA + αᵦB(1 - αₐ)           |
| Multiply      | A·B                         |
| Screen        | 1 - (1 - A)(1 - B)          |

## Testing Strategy

1. Unit Tests:
   - Font metric calculations
   - Coordinate transformations
   - Blend mode math

2. Integration Tests:
   - End-to-end text rendering
   - Undo/redo stack validation
   - Memory pressure tests

3. Fuzz Tests:
   - Invalid font inputs
   - Extreme coordinate values
   - Large text payloads

## Cross-Component Interactions

```mermaid
graph TD
    TextOverlay --> ThemeManager
    TextOverlay --> UndoStack
    TextOverlay --> SecurityEngine
    TextOverlay -->|notifies| GUIRenderer
