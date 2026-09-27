# PDF Renamer

A Windows desktop app that batch-renames PDF files and writes a **Title** (and optionally an **Author**) into each file's metadata. You define naming patterns once for the whole batch, and the app previews every result and flags problems before anything is changed.

For example, `scan7.pdf` with the pattern `Chapter {n} - {title}` and 2-digit padding becomes `Chapter 07 - Introduction.pdf`, and its Title metadata becomes `Chapter 07 - Introduction`.

## Features

- **Naming patterns** with the placeholders `{n}` (first number in the filename), `{title}` and `{author}`, plus optional zero-padding for `{n}`.
- **Title and Author patterns** that apply to every file at once, with per-file editing in the table and saved presets.
- **Pre-run checks.** The Status column predicts each file's outcome (`ready`, `unchanged`, `suffix`, `overwrite`) and shows problems (`no title`, `duplicate`, `exists`) in red before you run.
- **Conflict handling.** When a name is already taken, you can skip the file, add a number (`Title (2).pdf`) or overwrite.
- **Output folder mode** writes renamed copies and leaves the originals alone.
- **Safe writes.** Each file is written to a temporary file first and then moved into place, so a failure never leaves a half-written PDF.
- **Keeps existing metadata** such as Subject, Keywords, dates, and Author when it's left blank.
- Drag and drop, subfolder scanning, light and dark themes, an exportable log, and in-app help (F1).

See [HELP.md](HELP.md) for the full user guide.

## Getting started

Developed and tested on Python 3.14 with PySide6 6.11 and pypdf 6.

```bash
pip install -r requirements.txt
python pdf-renamer-v2.py
```

## Development

```bash
pip install -r requirements-dev.txt

python -m pytest tests            # run the test suite (the GUI tests run headless)
pyinstaller pdf-renamer-v2.spec   # build a single-file Windows .exe in dist/
python make_icon.py               # regenerate app.ico and icon.png after editing icon.svg
```

### Project layout

| File | Purpose |
|---|---|
| `pdf_renamer_core.py` | Renaming logic with no GUI dependencies: patterns, pre-run checks and file processing |
| `pdf-renamer-v2.py` | The PySide6 (Qt) GUI |
| `pdf-renamer.py` | The original tkinter version, kept for reference and no longer maintained |
| `tests/` | pytest suite for the core logic, plus GUI smoke tests |
| `HELP.md` | User help, shown in the app's Help window |
| `pdf-renamer-v2.spec` | PyInstaller build definition |

The version number is defined once, as `__version__` in `pdf_renamer_core.py`. The window title, the Help window and the `.exe`'s file properties all read it from there.

Settings are stored in `%APPDATA%\PDF Renamer\settings.ini`. Delete that file to reset the app to its defaults.

## License

PDF Renamer © 2026 Jim Finn is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE.md](LICENSE.md).

Created with the assistance of [Claude](https://claude.ai), an AI assistant made by Anthropic.

## Roadmap

- `{i}` placeholder for a file's position in the list
- Undo the last batch
- Background processing with a Cancel button
- Title suggestions from the first page's text
- Command-line mode with a dry run
- GitHub Actions for tests and release builds
