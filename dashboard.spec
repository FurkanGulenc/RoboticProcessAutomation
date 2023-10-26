# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['customTkinderGui/dashboard.py'],
    pathex=[],
    binaries=[],
    datas=[('./app/constant_data/logo_mizan.xlsx', 'constant_data'),
        ('./app/constant_data/Mapping.xlsx', 'constant_data'),
        ('./app', 'app'),
        ('./customTkinderGui', 'customTkinderGui')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dashboard',
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
