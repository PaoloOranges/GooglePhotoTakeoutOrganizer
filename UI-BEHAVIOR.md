# UI Behavior: Extension Selection

## Checkbox Pre-selection

**Location:** `get_selected_extensions()` function in `main.py`

**Behavior:** All file extensions are pre-selected by default EXCEPT those in `excluded_extensions` set.

**Current Excluded Extensions:**
- `.json` — Google Photos metadata files
- `.html` — HTML files

**Rationale:** Maximize media file coverage while excluding metadata/auxiliary files. Users can still:
- Deselect any pre-selected extensions they don't want
- Select any deselected extensions they want

## Implementation Details

The function uses `questionary.Choice` objects with the `checked=True` parameter for extensions that should be pre-selected. Each choice is created with:
```python
Choice(label, checked=is_checked)
```
where `is_checked` is `True` for all extensions except those in `excluded_extensions`.

The `Choice` class is imported from questionary:
```python
from questionary import Choice
```

## Modifying Excluded Extensions

To add or remove extensions from the exclusion list in future development:

1. Open `main.py`
2. Locate line: `excluded_extensions = {".json", ".html"}`
3. Add or remove extensions in the set (e.g., `{".json", ".html", ".xml"}`)
4. Re-run the script to verify the UI reflects the change

## Related Files
- `main.py` - Contains `get_selected_extensions()` function (lines 14-52)
