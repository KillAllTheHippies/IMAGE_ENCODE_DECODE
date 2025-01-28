# ADR 005: Package Structure Refinement

**Status:** Accepted

**Implementation Progress:**
- [x] Removed duplicate nested package structure
- [x] Updated core module imports (verified via import pattern analysis)
- [ ] Migrated GUI components to new interfaces
- [ ] Validated public API exports

**Next Implementation Steps:**

#### GUI Component Migration
1. Update GUI imports to use new core interfaces:
   ```python
   # Old pattern
   from steganography.encoder import encode_data
   
   # New pattern
   from steganography.core.encoder import encode_data
   ```
2. Refactor theme management to use new StyleManager class
3. Update dialog boxes to use consolidated resource loader

#### Public API Validation
1. Verify __init__.py exports in root package:
   ```python
   # steganography/__init__.py
   __all__ = ['encode_data', 'decode_data', 'SteganographyError']
   
   from .core.encoder import encode_data
   from .core.decoder import decode_data
   from .core.exceptions import SteganographyError
   ```
2. Validate type hint consistency across exported functions
3. Verify exception hierarchy matches architectural spec
**Date:** 2025-01-27

## Context
The current package structure exhibits several anti-patterns:
1. Duplicate nested `image_steganography/image_steganography/` paths
2. Core implementation scattered across 3 directories
3. Missing clear public API boundaries

## Decision
1. Consolidate package hierarchy:
   - Remove redundant `image_steganography/image_steganography/` subtree
   - Establish single source of truth under `steganography/`
     - Core algorithms: `steganography/core/`
     - GUI components: `steganography/gui/`
     - Utilities: `steganography/utils/`

2. Define public API in `steganography/__init__.py`:
```python
# Public interface exports
from .core.encoder import encode_data
from .core.decoder import decode_data
from .image_utils import (
    validate_image_format,
    SUPPORTED_FORMATS
)
from .exceptions import SteganographyError
```

3. Implementation requirements:
- Add type hints to all public functions
- Create exception hierarchy rooted in SteganographyError
- Update 12 test files with new import paths

## Consequences
- Breaking changes to existing CLI integration
- Requires coordinated updates across:
  - 6 core Python modules
  - 3 GUI components
  - Documentation in 4 markdown files
- Estimated migration effort: 8-10 developer hours