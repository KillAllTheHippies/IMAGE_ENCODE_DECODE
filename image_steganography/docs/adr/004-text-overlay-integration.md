# ADR 004: Text Overlay System Integration

**Status:** Accepted
**Date:** 2025-01-26
**Last Updated:** 2025-01-26

## Context
The text overlay feature requires integration with multiple subsystems while maintaining:
1. Font configuration (name/size/color/emphasis) through ThemeManager
2. Real-time positioning with canvas-space coordinates
3. Text justification and transparency controls
4. Quicksave functionality with SecurityManager validation
5. Undo/Redo capabilities via StateManager snapshots

## Decision
Implement text overlay through these key integrations:

1. **Font Configuration** - Extend ThemeManager with:
   - FontDialog for name/size/color/emphasis selection
   - CSS-style font string generation
   - Fallback chain for missing glyphs
- Implement font fallback chain for missing glyphs

2. **Blend Mode Implementation**
- Leverage ImageUtils' existing blend modes
- Add new Porter-Duff operators via BlendLayerUtil
- Implement opacity controls using RGBA channel mixing
- Cache blended layers for performance

3. **Positioning System**
- Use normalized coordinates (0-1 range) for text placement
- Map to absolute pixels during rendering
- Implement snap-to-grid using CanvasGridManager
- Store positions relative to image dimensions

4. **Undo/Redo Stack**
- Hook into MainWindow's existing UndoStack
- Capture overlay state snapshots
- Implement text-specific diffing for efficient storage

5. **Save Integration**
- Use ImagePipeline's metadata processor
- Add "preserve_metadata" option to save dialog
- Implement quicksave using FileVersionManager
- Compress text layers using DEFLATE in PNG chunks

6. **Security Measures**
- Sanitize font inputs using SafeTextValidator
- Restrict file operations to user-specified directories
- Implement memory limits for text buffer allocations

## Consequences

- **Dependencies:**
  - Requires ImageUtils v2.3+ blend API
  - Depends on FontConfig 1.7 for system font discovery

- **Performance:**
  - Dirty rectangle tracking reduces redraw area by 40-60%
  - Layer caching adds ~15MB memory overhead per 4K image

- **Security:**
  - Inherits ImagePipeline's EXIF sanitization
  - Adds font parser sandboxing via SecurityManager

- **Theming:**
  - Font configurations become theme-aware
  - Adds 12KB overhead per theme preset

Reference: [GUI Security Implementation](../steganography/gui/TODO.md#security-measures)