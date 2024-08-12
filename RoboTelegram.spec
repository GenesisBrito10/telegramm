# spec file for PyInstaller
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mainnn.py'],
    pathex=['/mnt/data/projeto_extracted'],
    binaries=[],
    datas=[
        ('database.db', '.'),
        ('Controller/*', 'Controller'),
        ('Database/*', 'Database'),
        ('Enums/*', 'Enums'),
        ('Lista/*', 'Lista'),
        ('Model/*', 'Model'),
        ('Threads/*', 'Threads'),
        ('Views/*', 'Views'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ROBOTELEGRAM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ROBOTELEGRAM'
)
