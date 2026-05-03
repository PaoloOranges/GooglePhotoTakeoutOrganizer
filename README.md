# GooglePhotoTakeoutOrganizer

A Python utility to organize and filter media files from Google Takeout exports. This script scans Google Photos takeout directories, displays file statistics, and selectively copies chosen media types into an organized output structure.

## Overview

This tool helps organize large Google Photos exports by:

- Scanning multiple takeout archives and computing file counts by extension
- Presenting an interactive selection (all extensions pre-selected except `.json` and `.html`)
- Copying selected media into `Media/` with special consolidation of `Untitled`/`Spotlight` folders
- Showing progress bars for folder processing and file copying

## Dependencies

- Python 3.7+
- `alive-progress`
- `piexif`
- `questionary>=2.0.0`

Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or manually:

```bash
pip install alive-progress piexif questionary>=2.0.0
```

## Quick start

Run the script against the folder that contains your extracted Google Takeout folders:

```bash
python3 main.py Root/
```

Where `Root/` contains subfolders like `takeout-.../Takeout/Google Photos/`.

### Workflow

1. Script scans source folders and prints file counts by extension.
2. An interactive `questionary` checkbox appears; all extensions are pre-selected except `.json` and `.html`.
3. The script gathers matching files and copies them into `Media/`, consolidating `Untitled`/`Spotlight` folders into `Media/Untitled/`.
4. Progress bars show folder processing and file copying.

### Example

Run a real example (replace `Root/` with your path):

```bash
python3 main.py Root/
```

Sample console excerpt:

```
.jpg is present 39886 times. 47.8%
.json is present 41716 times. 49.97%
.mp4 is present 598 times. 0.72%
[Interactive checkbox appears - all selected except .json and .html]

Selected extensions: .jpg, .mp4, .png

Processing Folders to gather media to copy...
|████████████████████| 45/45
Copying files...
|████████████████████| 30489/30489
```

## Input / Output structure

Input (example):

```
Root/
└── takeout-YYYYMMDDTHHMMSSZ-1/
	└── Takeout/Google Photos/
		├── Photos from 2020/
		└── Untitled(3)/
```

Output example:

```
Media/
├── Photos from 2020/
└── Untitled/
```

Folders matching `Untitled(\(\d\))?|Spotlight(\(\d\))?` are consolidated into `Media/Untitled/`.

## Configuration

The interactive defaults are controlled by `excluded_extensions` in `get_selected_extensions()` inside `main.py`:

```python
excluded_extensions = {".json", ".html"}
```

Edit that set to change which extensions are not pre-selected.

## Performance & large runs

- Verify you have sufficient disk space for the output.
- For very large exports, run on an SSD and consider processing in batches.
- The script builds an in-memory list of copy operations; this is usually modest but grows with file count.

## Troubleshooting

- Missing dependency: `pip install -r requirements.txt`
- No interactive menu: ensure you're running in an interactive terminal (not redirected input).
- Permission denied: check write permissions to the working directory.

## For developers

- `main()` – orchestration
- `get_selected_extensions()` – interactive UI (uses `questionary.Choice(..., checked=...)`)
- `filter_only_media_files()` – extension filtering
- `copy_file()` – single-file copy operation

See `UI-BEHAVIOR.md` for notes on the interactive selection behavior.

## License

This project is MIT-licensed. See `LICENSE` for details.

---

Note: This `README.md` file was generated with assistance from an AI tool to speed documentation. Review and edit as needed.

