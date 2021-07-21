# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# added_files = [('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo2.png', '.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\schema.png', '.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\v2\\train.xml','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_head.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_LS.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_scale.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\GBClassifierFinal.joblib','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\SVCClassifierFinal.joblib','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\XGBClassifierFinal.joblib','.'),('C:\\Users\\MASSON\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\xgboost','xgboost')]
# added_files = [('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo2.png', '.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\schema.png', '.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\v2\\train.xml','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_head.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_LS.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_scale.dat','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\GBClassifierFinal.joblib','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\SVCClassifierFinal.joblib','.'),('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\XGBClassifierFinal.joblib','.')]

added_files = [('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo2.png', '.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\schema.png', '.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo_import.png','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo_predict.png','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo_left_arrow.png','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\images\\logo_right_arrow.png','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\v2\\train.xml','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_head.dat','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_LS.dat','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\predictor_scale2.dat','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\GBClassifierFinal2.joblib','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\SVCClassifierFinal2.joblib','.'),
               ('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\models\\XGBClassifierFinal2.joblib','.'),
               ('C:\\Users\\MASSON\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\xgboost','xgboost')]

a = Analysis(['GUI_normal.py'],
             pathex=['C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\code\\GUI_normal.py'],
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
