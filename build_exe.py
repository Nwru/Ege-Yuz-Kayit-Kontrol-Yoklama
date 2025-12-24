"""
PyInstaller ile exe dosyası oluşturma scripti
"""
import PyInstaller.__main__
import os

# PyInstaller parametreleri
args = [
    'main.py',                    # Ana dosya
    '--name=YuzTanimaSistemi',    # Exe dosya adı
    '--onefile',                  # Tek dosya olarak paketle
    '--windowed',                 # Konsol penceresi gösterme (GUI için)
    '--icon=NONE',                # İkon yok (isteğe bağlı eklenebilir)
    '--add-data=dataset;dataset', # Dataset klasörünü dahil et (varsa)
    '--hidden-import=tkinter',    # Tkinter'ı açıkça dahil et
    '--hidden-import=cv2',        # OpenCV'yi açıkça dahil et
    '--hidden-import=numpy',      # NumPy'yi açıkça dahil et
    '--collect-all=cv2',          # OpenCV'nin tüm modüllerini topla
    '--collect-all=tkinter',      # Tkinter'ın tüm modüllerini topla
]

PyInstaller.__main__.run(args)

