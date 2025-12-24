@echo off
echo PyInstaller ile exe dosyasi olusturuluyor...
echo.

REM PyInstaller yuklu mu kontrol et
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller yukleniyor...
    pip install pyinstaller
)

REM Exe dosyasini olustur
python -m PyInstaller main.py ^
    --name=YuzTanimaSistemi ^
    --onefile ^
    --windowed ^
    --hidden-import=tkinter ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --collect-all=cv2 ^
    --collect-all=tkinter

echo.
echo Islem tamamlandi!
echo Exe dosyasi: dist\YuzTanimaSistemi.exe
pause

