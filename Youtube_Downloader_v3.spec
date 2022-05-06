# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/Youtube_Downloader_v3.py'],
             pathex=[],
             binaries=[],
             datas=[('C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/YoutubeVenv/Lib/site-packages/customtkinter', 'customtkinter/'), ('C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/youtube.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Youtube_Downloader_v3',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\ertug\\G_Drive\\Code\\Python\\Youtube_Downloader_v3_venv\\Youtube_Downloader_v3\\youtube.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Youtube_Downloader_v3')
