# PDF Renamer: Project Summary

This is a handover summary written when the project moved out of the `Coding-Projects` repo into its own repository (September 2026). It records what the app is, how it is organised, the decisions behind it, and what is planned next.

## What the app does

PDF Renamer batch-renames PDF files and writes a **Title** (and optionally an **Author**) into each file's metadata. You define naming patterns once for the whole batch, and the app previews the result and flags problems before anything is changed.

Example: `scan7.pdf` with the pattern `Chapter {n} - {title}` and 2-digit padding becomes `Chapter 07 - Introduction.pdf`, and its Title metadata becomes `Chapter 07 - Introduction`.

## Project structure

| File | Purpose |
|---|---|
| `pdf_renamer_core.py` | All renaming logic with no GUI dependencies: patterns, pre-run checks, file processing. Safe to import and test on its own. |
| `pdf-renamer-v2.py` | The PySide6 (Qt) GUI. Run this to launch the app. |
| `pdf-renamer.py` | The original tkinter version, kept for reference. Not maintained. |
| `tests/test_core.py` | 41 pytest tests for the core logic |
| `tests/test_gui_smoke.py` | 6 headless GUI tests: a full batch end to end, presets, titles from filename parts, problem summary, Title column fitting, and the About window |
| `README.md` | GitHub landing page: overview, features, setup and development commands |
| `HELP.md` | User help, shown in the app's Help window (F1). Edit this file to update the in-app help. |
| `pdf-renamer-v2.spec` | PyInstaller build definition (bundles `app.ico` and `HELP.md`) |
| `icon.svg` | Source artwork for the icon |
| `make_icon.py` | Regenerates `app.ico` (9 sizes) and `icon.png` from `icon.svg` |
| `LICENSE.md` | CC BY-NC-SA 4.0 licence summary and link to the legal code |
| `requirements.txt` / `requirements-dev.txt` | Runtime dependencies / plus pytest and PyInstaller |

## Running, testing and building

```bash
pip install -r requirements-dev.txt

python pdf-renamer-v2.py            # run the app
python -m pytest tests              # run all 47 tests (the GUI tests run headless)
pyinstaller pdf-renamer-v2.spec     # build dist/pdf-renamer-v2.exe (single file, ~50 MB);
                                    # rename to PDF-Renamer-<version>.exe for a GitHub Release
python make_icon.py                 # only after editing icon.svg
```

Developed and tested on Python 3.14 with PySide6 6.11 and pypdf 6; minimums are `pypdf>=6.0` and `PySide6>=6.5`.

## Features

**Renaming**
- Placeholders `{n}` (first number in the filename), `{title}` and `{author}`, with an optional zero-padding width for `{n}`. An explicit format like `{n:03d}` overrides the padding.
- **Titles from the filename:** `{name}` (the whole stem) and `{part1}`, `{part2}`, ... (pieces of the stem). **Divide filename into parts at** picks the dividers: dash or underscore (default), dash, underscore, space, full stop, any of those, or custom characters. Parts are stripped and empty ones dropped; a part past the end is blank. A preview line shows how the first file divides. Presets and settings store the dividers.
- Title and Author patterns, applied to all files at once or edited per file in the table.
- Saved **presets** of title pattern, author pattern, padding and filename dividers.
- Invalid filename characters are removed from the filename only; the Title metadata keeps them.
- Existing metadata (Subject, Keywords, dates, and Author when left blank) is preserved.

**Safety**
- **Pre-run checks** (`check_batch`): the Status column predicts each file's outcome before you run: `ready`, `unchanged`, `suffix`, `overwrite`, or a problem: `no title`, `duplicate`, `exists`. Problems are shown in red and counted, and Run asks for confirmation if any remain.
- **Conflict handling:** skip, add a number (`Title (2).pdf`), or overwrite. Overwrite refuses to replace another listed file that hasn't been renamed yet.
- **Output folder mode:** writes renamed copies and keeps the originals.
- Each file is written to a temporary file first and then moved into place, so a failure never leaves a half-written or clobbered PDF.

**Interface**
- Opens maximized. Naming Patterns sit beside a Batch panel (add files, Run, progress), with the file table and log below.
- Drag and drop files or folders; optional subfolder scanning; natural, alphabetical or date sort.
- Light, dark, or follow-system themes, with 3D sunken and raised styling.
- A log you can resize, hide and export, with timestamps.
- Remembered column widths, with a reset option in Settings.
- App icon, and a Help window rendered from `HELP.md`.
- An About window: version, author, repository link, licence, the Claude credit, and Python/PySide6/pypdf versions.

**Saved state:** stored with `QSettings` in `%APPDATA%\PDF Renamer\settings.ini`: preferences, presets, last patterns, window layout, column widths and log size. It lives outside the repo, so it isn't affected by the move. Delete the file to reset to defaults.

## Versioning

The version is defined once, as `__version__` in `pdf_renamer_core.py`, using `MAJOR.MINOR.PATCH` (semantic versioning). It is currently **2.1.0**: the tkinter app counts as 1.x, the PySide6 rewrite is 2.0.0, and 2.1.0 adds titles from the filename and clearer naming problems.

It appears in the main window title, at the bottom of the Help window, and in the `.exe`'s Properties > Details tab (`pdf-renamer-v2.spec` reads it at build time). To release, bump the number and tag the commit to match the existing `V2.0.0` style (e.g. `V2.1.0`). Bump PATCH for fixes, MINOR for new features, and MAJOR for breaking changes.

## Licence and credits

Licensed under CC BY-NC-SA 4.0 (see `LICENSE.md`); author Jim Finn. The app notes that it was created with the assistance of Claude (Anthropic). The author, repository URL and licence are defined as constants next to `__version__` in `pdf_renamer_core.py`, and the About window and `.exe` build both read them from there. Creative Commons advises against CC licences for software; this licence was chosen deliberately, to suit sharing among teachers.

## Design decisions

- **Core and GUI kept separate.** `pdf_renamer_core.py` has no Qt imports, so it can be tested and used headless (e.g. for a future command-line mode).
- **`check_batch` predicts and `process_file` acts.** Both use the same `target_path` and `unique_path` helpers, so the Status column matches what actually happens.
- **Windows-first.** Filename comparisons ignore upper/lower case, the app has its own taskbar identity so its icon shows, and the `.exe` build is Windows-only. The Python code itself is cross-platform.
- **Qt stylesheet limits.** Drop-downs, spin boxes and checkboxes are deliberately left in the standard Fusion style, because stylesheet-styling them breaks their arrows and indicators.
- **A collapsed log re-fits itself whenever its layout changes size.** This fixed squashed buttons when the app started with the log hidden, because sizes measured before the stylesheet is applied are too small.

## History

| Commit | Change |
|---|---|
| `d4c7d9f` | Original tkinter app (`pdf-renamer.py`) and first v2 |
| `dd42935` | Rewrite in PySide6: pre-run checks, conflict modes, output folder, settings, presets, themes, icon, help |
| `dd3c8d3` | Core logic split into `pdf_renamer_core.py`; pytest suite added. The tests found and fixed a bug: renaming wiped all existing metadata except Title/Author. |
| `f9136c1` (tag `V2.0.0`, GitHub Release 2.0.0) | `.gitignore` now covers `dist/`, `__pycache__/`, `*.pyc` and virtual environments. Added `README.md` (seeded from this summary and `HELP.md`) and this `PROJECT_SUMMARY.md`. Version **2.0.0** introduced (see Versioning). Added an **About** button and window, licensed the project under **CC BY-NC-SA 4.0** (`LICENSE.md`), and stamped the author and licence into the `.exe`'s file properties. Built `dist/PDF-Renamer-2.0.0.exe` (48.2 MB, SHA-256 `083E8814…282532E`) for the v2.0.0 GitHub Release. Added `.gitattributes` (`* text=auto`, binaries marked) so line endings are normalised. |
| `c2598af` | Removed the old tkinter build `dist/PDF Renamer.exe` from the repo (builds are now published as GitHub Release assets). |
| *(next commit)* (to tag `V2.1.0`) | Version **2.1.0**. **Titles from the filename:** new `{name}` and `{part1}`, `{part2}`, ... placeholders, with a **Divide filename into parts at** option (preset choices or custom characters) and a parts preview line. `split_filename()` added to the core, and `apply_pattern()` takes `dividers`. Dividers are saved in presets (older presets default to dash or underscore) and settings. Fixed: a pattern like `{title.x}` crashed instead of reporting an invalid pattern. **Clearer naming problems:** the summary under Run now counts each kind (e.g. "68 duplicate names"), its tooltip explains each kind and how to fix it, and a **Show the first one** link selects that row and scrolls Status into view. Fixed: a Title column dragged (or saved) wider than the window pushed Status off-screen; Title now shrinks back to fit whenever the window or another column changes size. 13 new tests (47 total). |

The history was carried over from `Coding-Projects` (`pdf renamer/` folder) using `git subtree split`, so the hashes differ from the original repo.

## Known issues and loose ends

- Processing runs on the GUI thread, so the window can stutter on very large PDFs and there's no Cancel.
- Move Up/Down only change the processing order, which has no visible effect on output names until an `{i}` placeholder exists (see Roadmap).

## Roadmap

In suggested order:

1. **`{i}` placeholder for list position**, so Move Up/Down control the numbering.
2. **Undo the last batch**, reverting renames (or deleting copies) using the recorded old → new names.
3. **Background processing with a Cancel button**, using a `QThread` worker.
4. **Suggest a title from the first page's text**, for scans with empty or junk metadata.
5. **Multi-select rows and a right-click menu:** open the PDF, show it in Explorer, remove.
6. **Subject and Keywords columns**, and a metadata-only mode (no rename).
7. **Command-line mode** with a dry run, built on `pdf_renamer_core`.
8. **GitHub Actions:** run the tests on every push, and build and attach the `.exe` when a release is tagged.
