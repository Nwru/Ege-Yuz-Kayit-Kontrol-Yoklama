# Yüz Tanıma ve Yoklama Sistemi

## Proje Tanımı

Bu proje, OpenCV kullanarak gerçek zamanlı yüz tanıma ve otomatik yoklama sistemi geliştiren bir Python uygulamasıdır. Sistem, web kamerası kullanarak kişileri tanır ve yoklama kayıtlarını tutar.

## Özellikler

### 1. Yüz Kaydetme
- Kullanıcıların isim ve öğrenci numarası ile kayıt yapabilmesi
- Web kamerasından 40 örnek görüntü toplama (3 saniye içinde)
- Yüz algılama ve otomatik kırpma
- Histogram eşitleme ile ışık normalleştirme
- Görüntülerin `dataset/<öğrenciNo>_<isim>/` klasörüne kaydedilmesi

### 2. Yüz Tanıma
- LBPH (Local Binary Patterns Histograms) yüz tanıma algoritması kullanımı
- Gerçek zamanlı video akışından yüz tanıma
- Tanınan kişilerin ekranda gösterilmesi
- Güven skoru gösterimi

### 3. Otomatik Yoklama Sistemi
- Gerçek zamanlı yoklama takibi
- Ardışık tanıma kontrolü (5 kare tutarlı tanıma gereksinimi)
- Tanınan kişilerin checkbox'larla işaretlenmesi
- Bilinmeyen kişi sayısının takibi
- Yoklama kayıtlarının CSV ve TXT formatında saklanması

## Teknik Detaylar

### Kullanılan Teknolojiler
- **Python 3.x**
- **OpenCV (opencv-contrib-python)**: Yüz algılama ve tanıma
- **NumPy**: Görüntü işleme
- **Tkinter**: Grafik kullanıcı arayüzü
- **CSV**: Veri kayıt formatı

### Algoritma
- **Yüz Algılama**: Haar Cascade Classifier (`haarcascade_frontalface_default.xml`)
- **Yüz Tanıma**: LBPH Face Recognizer
- **Görüntü İşleme**: 
  - Gri tonlama
  - 200x200 piksel boyutlandırma
  - Histogram eşitleme

### Ayarlar
- `CONF_THRESHOLD = 70`: Tanıma güven eşiği (düşük değer = daha iyi eşleşme)
- `CONSISTENT_FRAMES = 5`: Yoklama için gereken ardışık tanıma sayısı
- `samples = 40`: Kayıt sırasında alınacak örnek sayısı
- `duration = 3.0`: Kayıt süresi (saniye)

## Proje Yapısı

```
Yüz tanıma projesi/
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Python bağımlılıkları
├── build.bat              # Windows exe oluşturma scripti
├── build.sh               # Linux/Mac exe oluşturma scripti
├── build_exe.py           # Python exe oluşturma scripti
├── dataset/               # Yüz görüntüleri veri seti
│   └── <öğrenciNo>_<isim>/
│       └── *.jpg         # Kişiye ait görüntüler
├── attendance_logs.csv    # Yoklama kayıtları (CSV formatı)
└── attendance_logs.txt    # Yoklama kayıtları (okunabilir format)
```

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
python main.py
```

## EXE Dosyası Oluşturma

Projeyi Windows'ta çalıştırılabilir bir .exe dosyasına dönüştürmek için:

### Windows için:

1. PyInstaller'ı yükleyin (requirements.txt ile birlikte yüklenir):
```bash
pip install -r requirements.txt
```

2. `build.bat` dosyasını çalıştırın:
```bash
build.bat
```

Veya manuel olarak:
```bash
python -m PyInstaller main.py --name=YuzTanimaSistemi --onefile --windowed --hidden-import=tkinter --hidden-import=cv2 --hidden-import=numpy --collect-all=cv2 --collect-all=tkinter
```

3. Oluşturulan exe dosyası `dist` klasöründe bulunacaktır: `dist\YuzTanimaSistemi.exe`

### Notlar:
- Exe dosyası ilk çalıştırmada biraz yavaş açılabilir (paketlenmiş modüllerin açılması nedeniyle)
- Exe dosyası ile birlikte `dataset` klasörü ve yoklama log dosyaları aynı dizinde oluşturulacaktır
- Web kamerası erişimi için gerekli izinlerin verildiğinden emin olun

## Kullanım

### 1. Yüz Kaydetme
- Ana pencerede "1) Yüz Kaydet" butonuna tıklayın
- İsim girin
- Öğrenci numarası girin
- Kameraya bakın ve 3 saniye bekleyin
- 40 örnek görüntü otomatik olarak kaydedilecektir
- Çıkmak için 'q' tuşuna basın

### 2. Yüz Tanıma ve Yoklama
- Ana pencerede "2) Yüz Tanıma" butonuna tıklayın
- Yoklama listesi penceresi açılacaktır
- "Başlat" butonuna tıklayarak tanımayı başlatın
- Tanınan kişiler otomatik olarak işaretlenecektir
- "Durdur" butonuna tıklayarak yoklamayı durdurun ve kaydedin
- Çıkmak için 'q' tuşuna basın

## Çıktı Formatları

### CSV Formatı (attendance_logs.csv)
```csv
timestamp,recognized_count,recognized_names,unknown_count
2025-12-22T15:49:03.093300,1,Ramazan (19240000836),0
```

### TXT Formatı (attendance_logs.txt)
```
Timestamp: 2025-12-22T15:49:03.093300
Recognized count: 1
Recognized names:
- Ramazan (19240000836)
Unknown count: 0
```

## Özellikler ve Limitasyonlar

### Güçlü Yönler
- Gerçek zamanlı yüz tanıma
- Otomatik yoklama kayıt sistemi
- Çoklu kişi tanıma desteği
- Kullanıcı dostu grafik arayüz
- Tutarlı tanıma kontrolü ile hata azaltma

### Limitasyonlar
- Sadece web kamerası desteği
- Işık koşullarına duyarlılık
- Yüz açısı ve pozisyonuna bağımlılık
- LBPH algoritmasının sınırlı doğruluk oranı

## Geliştirici Notları

- Sistem, her kişi için en az 40 örnek görüntü ile eğitilmelidir
- Daha iyi sonuçlar için farklı açılardan ve ışık koşullarında görüntü toplanmalıdır
- Güven eşiği değeri, tanıma hassasiyetini ayarlamak için değiştirilebilir
- Ardışık tanıma sayısı, yanlış pozitifleri azaltmak için ayarlanabilir

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

