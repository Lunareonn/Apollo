# -*- mode: python ; coding: utf-8 -*-

import os
import pykakasi
import ytmusicapi

pykakasi_pkg = os.path.dirname(pykakasi.__file__)
pykakasi_data_dir = os.path.join(pykakasi_pkg, "data")
pykakasi_datas = []
if os.path.isdir(pykakasi_data_dir):
    for root, _, files in os.walk(pykakasi_data_dir):
        rel_root = os.path.relpath(root, pykakasi_pkg)
        for fn in files:
            src = os.path.join(root, fn)
            # destination inside the bundle: keep the package layout
            dest = os.path.join("pykakasi", rel_root)
            pykakasi_datas.append((src, dest))

ytmusicapi_pkg = os.path.dirname(ytmusicapi.__file__)
ytmusicapi_locale_dir = os.path.join(ytmusicapi_pkg, "locales")
ytmusicapi_datas = []
if os.path.isdir(ytmusicapi_locale_dir):
    for root, _, files in os.walk(ytmusicapi_locale_dir):
        rel_root = os.path.relpath(root, ytmusicapi_pkg)
        for fn in files:
            src = os.path.join(root, fn)
            dest = os.path.join("ytmusicapi", rel_root)
            ytmusicapi_datas.append((src, dest))

datas = (locals().get("datas") or []) + pykakasi_datas + ytmusicapi_datas

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

a.datas += Tree('src/frontend/assets', 'assets')
a.datas += Tree('src/frontend/html', 'html')

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='apollo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
