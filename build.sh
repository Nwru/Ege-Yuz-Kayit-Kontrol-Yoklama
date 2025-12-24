#!/bin/bash
echo "PyInstaller ile exe dosyası oluşturuluyor..."
echo ""

# PyInstaller yüklü mü kontrol et
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller yükleniyor..."
    pip install pyinstaller
fi

# Exe dosyasını oluştur
python3 -m PyInstaller main.py \
    --name=YuzTanimaSistemi \
    --onefile \
    --windowed \
    --hidden-import=tkinter \
    --hidden-import=cv2 \
    --hidden-import=numpy \
    --collect-all=cv2 \
    --collect-all=tkinter

echo ""
echo "İşlem tamamlandı!"
echo "Exe dosyası: dist/YuzTanimaSistemi.exe"

