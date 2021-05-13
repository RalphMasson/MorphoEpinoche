# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo2.png', '.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\schema.png', '.')]

a = Analysis(['Interface_Sexage.py'],
             pathex=['C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\code\\Interface_Sexage.py'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Morphométrie_Ineris',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
