# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],           # 메인 스크립트
    pathex=[],             # 추가 경로
    binaries=[],           # 바이너리 파일
    datas=[
    ('keycab.ico', '.'),
    ('data/', 'data'),
    ('font/', 'font'),
    ('img/', 'img'),
    ('sound/', 'sound')
    ],              # 포함할 데이터 파일 (이미지, 폰트, 설정 파일 등)
    hiddenimports=[
        'pygame'
    ],                     # 명시적으로 추가할 숨겨진 모듈
    hookspath=[],          # 사용자 정의 hook 경로
    runtime_hooks=[],      # 런타임 hook
    excludes=[],           # 제외할 모듈
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='Typing_monster',          # 실행 파일 이름
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # 콘솔 창 표시 여부
    icon='keycab.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Typing_monster',
)
