# -*- mode: python ; coding: utf-8 -*-

import sys

from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo, StringFileInfo, StringStruct, StringTable, VarFileInfo, VarStruct,
    VSVersionInfo,
)

# Read the version from the core module so it's only defined in one place.
sys.path.insert(0, SPECPATH)
from pdf_renamer_core import AUTHOR, LICENSE_NAME, __version__

version_tuple = tuple(int(part) for part in __version__.split(".")) + (0,)

# Shown in the .exe's Properties > Details tab in Explorer.
version_info = VSVersionInfo(
    ffi=FixedFileInfo(filevers=version_tuple, prodvers=version_tuple),
    kids=[
        StringFileInfo([StringTable("040904B0", [
            StringStruct("FileDescription", "PDF Renamer"),
            StringStruct("ProductName", "PDF Renamer"),
            StringStruct("FileVersion", __version__),
            StringStruct("ProductVersion", __version__),
            StringStruct("CompanyName", AUTHOR),
            StringStruct("LegalCopyright", f"© {AUTHOR}. Licensed under {LICENSE_NAME}."),
            StringStruct("OriginalFilename", "pdf-renamer-v2.exe"),
        ])]),
        VarFileInfo([VarStruct("Translation", [0x0409, 1200])]),
    ],
)


a = Analysis(
    ['pdf-renamer-v2.py'],
    pathex=[],
    binaries=[],
    # Loaded at runtime via resource_path(): window/taskbar icon and the Help window's text.
    datas=[('app.ico', '.'), ('HELP.md', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf-renamer-v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',  # the .exe's icon in Explorer
    version=version_info,
)
