"""Smoke test: build the main window headlessly and run a small batch end to end."""

import importlib.util
import os
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")  # no window on screen

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from test_core import make_pdf, meta, names  # noqa: E402

APP_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def gui():
    """The pdf-renamer-v2 module (hyphenated filename, so loaded by path)."""
    spec = importlib.util.spec_from_file_location("pdf_renamer_gui", APP_DIR / "pdf-renamer-v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def window(gui, tmp_path):
    app = QApplication.instance() or QApplication([])
    # Keep the user's real %APPDATA% settings out of it.
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path / "settings"))
    w = gui.App()
    w._confirm_run_with_problems = lambda problems: True  # no modal dialog in tests
    yield w
    w.close()
    app.processEvents()


def cells(w, column):
    return [w._cell(r, column) for r in range(w.table.rowCount())]


def test_batch_end_to_end(window, tmp_path):
    folder = tmp_path / "pdfs"
    folder.mkdir()
    for n in ("scan10", "scan2", "copy2"):
        make_pdf(folder / f"{n}.pdf")

    window._add_folder(folder)
    assert cells(window, "file") == ["copy2.pdf", "scan2.pdf", "scan10.pdf"]  # natural sort
    assert window.file_count_label.text() == "3 files"

    window.title_pattern_edit.setText("Doc {n}")
    window.pad_spin.setValue(2)
    window.apply_batch_title_pattern()
    assert cells(window, "title") == ["Doc 02", "Doc 02", "Doc 10"]
    assert cells(window, "status") == ["duplicate", "duplicate", "ready"]

    window.prefs["on_conflict"] = "suffix"
    window._validate()
    assert cells(window, "status") == ["ready", "suffix", "ready"]

    window.run_batch()
    assert cells(window, "status") == ["renamed", "renamed", "renamed"]
    assert names(folder) == ["Doc 02 (2).pdf", "Doc 02.pdf", "Doc 10.pdf"]
    assert meta(folder / "Doc 10.pdf")[0] == "Doc 10"


def test_presets_round_trip(window, gui, monkeypatch):
    window.title_pattern_edit.setText("Chapter {n}")
    window.pad_spin.setValue(3)
    monkeypatch.setattr(gui.QInputDialog, "getText", staticmethod(lambda *a, **k: ("Chapters", True)))
    window.save_preset()
    window.title_pattern_edit.clear()
    window.pad_spin.setValue(0)

    window.preset_combo.setCurrentIndex(window.preset_combo.findData("Chapters"))
    window._on_preset_chosen(0)
    assert window._current_patterns() == {"title": "Chapter {n}", "author": "", "pad": 3,
                                          "dividers": gui.DEFAULT_DIVIDERS}


def test_title_from_filename_parts(window, tmp_path):
    folder = tmp_path / "pdfs"
    folder.mkdir()
    make_pdf(folder / "Smith - 2024 - Report.pdf")
    window._add_folder(folder)

    window.title_pattern_edit.setText("{part3} ({part2}) by {part1}")
    window.apply_batch_title_pattern()
    assert cells(window, "title") == ["Report (2024) by Smith"]  # default divides at - or _

    window._set_dividers(" ")  # a choice from the list
    assert cells(window, "title") == ["2024 (-) by Smith"]  # titles follow the new divider
    window._set_dividers("~")  # not in the list: Custom
    assert window.divider_combo.currentData() is None and window.divider_edit.isEnabled()
    assert cells(window, "title") == [" () by Smith - 2024 - Report"]
    assert "{part1} = Smith - 2024 - Report" in window.parts_sample.text()


def test_shared_metadata_titles_explain_the_problem(window, tmp_path):
    folder = tmp_path / "pdfs"
    folder.mkdir()
    for n in ("History of Ghosts", "History of Vampires"):
        make_pdf(folder / f"{n}.pdf", title="downmagaz.net")  # same junk Title in every file
    window._add_folder(folder)

    assert cells(window, "status") == ["duplicate", "duplicate"]
    assert "2 naming problems: 2 duplicate names<br>" in window.issue_label.text()
    assert "{name}" in window.issue_label.toolTip()  # suggests a fix
    window.show_first_problem()
    assert window._selected_row() == 0

    window.title_pattern_edit.setText("{name}")
    window.apply_batch_title_pattern()
    assert cells(window, "status") == ["unchanged", "unchanged"]
    assert window.issue_label.text() == ""


def test_title_column_shrinks_so_status_stays_visible(window, gui):
    window.resize(1200, 700)
    window.show()
    window.title_width = 5000  # e.g. dragged wide on a bigger screen
    window._fit_title_column()
    header = window.table.horizontalHeader()
    total = sum(header.sectionSize(i) for i in range(header.count()))
    # Title fits within the table again (unless even its minimum width doesn't fit).
    assert total <= window.table.viewport().width() or window.title_width == gui.TITLE_MIN_WIDTH
    assert window.title_width < 5000


def test_about_dialog(window, gui):
    dialog = gui.AboutDialog(window)
    text = dialog.findChildren(gui.QLabel)[-1].text()
    assert gui.REPO_URL in text
    assert gui.LICENSE_NAME in text
    assert "Claude" in text
    dialog.close()
