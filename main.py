import os
import cv2
import time
import csv
import datetime
import re
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

DATASET_DIR = "dataset"
os.makedirs(DATASET_DIR, exist_ok=True)
ATTENDANCE_LOG = "attendance_logs.csv"
ATTENDANCE_LOG_TXT = "attendance_logs.txt"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Ayarlar: bu değerleri ihtiyaca göre artırıp azaltabilirsiniz
CONF_THRESHOLD = 70  # LBPH için daha düşük değer daha iyi eşleşme
CONSISTENT_FRAMES = 5  # aynı kişiden kaç ardışık/tekrarlanan tanıma gelecekse yoklama işareti atılsın
UNKNOWN_LABEL = "?"


def capture_and_save(name, student, samples=40, duration=3.0):
    # Klasör adı: <ogrenciNo>_<isim>    import cv2, time, threading
    
    def warmup_camera(index=0, frames=10, delay=0.05, width=320, height=240, keep_open=False):
        """
        Kamerayı hızlıca açıp birkaç kare okuyarak ısıtır.
        - index: kamera indeksi
        - frames: kaç kare okunacağı
        - delay: kareler arası bekleme (saniye)
        - keep_open: True ise kapatmaz, VideoCapture döner
        """
        cap = cv2.VideoCapture(index)
        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        except Exception:
            pass
        for _ in range(frames):
            ret, _ = cap.read()
            time.sleep(delay)
        if keep_open:
            return cap
        try:
            cap.release()
        except Exception:
            pass
        return None
    person_dir = os.path.join(DATASET_DIR, f"{student}_{name}")
    os.makedirs(person_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)
    count = len([f for f in os.listdir(person_dir) if os.path.isfile(os.path.join(person_dir, f))])
    saved = 0
    last_save_time = 0.0
    # İstenen sürede eşit aralıklarla fotoğraf al
    interval = max(0.01, float(duration) / max(1, samples))
    while saved < samples:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        # Eğer yüz algılanmışsa ve zaman aralığı geçtiyse en büyük yüzü kaydet
        if len(faces) > 0 and (time.time() - last_save_time >= interval):
            # En büyük yüzü seç (büyük alan)
            faces_sorted = sorted(faces, key=lambda r: r[2] * r[3], reverse=True)
            x, y, w, h = faces_sorted[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_img = gray[y:y + h, x:x + w]
            try:
                face_resized = cv2.resize(face_img, (200, 200))
            except Exception:
                face_resized = face_img
            # Işık koşullarını biraz normalize etmek için histogram eşitleme uygula
            try:
                face_resized = cv2.equalizeHist(face_resized)
            except Exception:
                pass
            # Dosya adında öğrenci numarası ve isim bulunsun
            filename = os.path.join(person_dir, f"{student}_{name}_{count+saved}.jpg")
            cv2.imwrite(filename, face_resized)
            saved += 1
            last_save_time = time.time()
        cv2.putText(frame, f"Saved: {saved}/{samples}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow(f"Kaydet - {name}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Bitti", f"{name} için {saved} örnek kaydedildi.")


def train_recognizer():
    faces = []
    labels = []
    label_map = {}
    current_label = 0
    for person_name in sorted(os.listdir(DATASET_DIR)):
        person_dir = os.path.join(DATASET_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue
        # person_name formatı: "<ogrenciNo>_<isim>" ise daha okunabilir göster
        if "_" in person_name:
            student_no, display_name = person_name.split("_", 1)
            label_map[current_label] = f"{display_name} ({student_no})"
        else:
            label_map[current_label] = person_name
        for fn in os.listdir(person_dir):
            path = os.path.join(person_dir, fn)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            # Işık farklılıklarını azaltmak için eğitim görüntülerine eşitleme uygula
            try:
                img = cv2.equalizeHist(img)
            except Exception:
                pass
            faces.append(img)
            labels.append(current_label)
        current_label += 1
    if len(faces) == 0:
        return None, None
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except Exception:
        messagebox.showerror("Hata", "opencv-contrib-python yüklü değil veya OpenCV'nin face modülü bulunamadı. Lütfen `pip install opencv-contrib-python` yapın.")
        return None, None
    recognizer.train(faces, np.array(labels))
    return recognizer, label_map


def recognize_loop(recognizer, label_map):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            face_resized = cv2.resize(face_img, (200, 200))
            try:
                label, conf = recognizer.predict(face_resized)
                # Eğer güven eşik değerinden yüksekse bilinmiyor/şüpheli kabul et
                if conf >= CONF_THRESHOLD:
                    text = f"{UNKNOWN_LABEL}"
                else:
                    name = label_map.get(label, "Bilinmiyor")
                    text = f"{name} ({conf:.1f})"
            except Exception:
                text = f"{UNKNOWN_LABEL}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.imshow("Tanıma", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def _attendance_thread(recognizer, label_map, var_map, stop_event, tk_root, unknown_label):
    cap = cv2.VideoCapture(0)
    # sayaçlar: her label için ardışık/tutarlı tanıma sayısını tut
    recognized_counts = {lab: 0 for lab in var_map.keys()}
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        # Bu karede hangi label'ların güvenli eşleşme aldığı
        incremented = set()
        unknown_count = 0
        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            face_resized = cv2.resize(face_img, (200, 200))
            face_resized = cv2.equalizeHist(face_resized)
            try:
                label, conf = recognizer.predict(face_resized)
                # Eğer güvenlik eşiğinin üzerinde ise bilinmiyor kabul et
                if conf >= CONF_THRESHOLD:
                    unknown_count += 1
                    text = f"{UNKNOWN_LABEL}"
                else:
                    if label in recognized_counts:
                        incremented.add(label)
                    text = f"{label_map.get(label, 'Bilinmiyor')} ({conf:.1f})"
            except Exception:
                unknown_count += 1
                text = f"{UNKNOWN_LABEL}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        # Sayaçları güncelle
        for lab in list(recognized_counts.keys()):
            if lab in incremented:
                recognized_counts[lab] = min(recognized_counts[lab] + 1, CONSISTENT_FRAMES)
            else:
                recognized_counts[lab] = max(recognized_counts[lab] - 1, 0)
            if recognized_counts[lab] >= CONSISTENT_FRAMES and not var_map[lab].get():
                tk_root.after(0, var_map[lab].set, True)
        # Bilinmeyen kişi sayısını güncelle (UI thread üzerinden)
        try:
            tk_root.after(0, unknown_label.config, {"text": f"{UNKNOWN_LABEL} : {unknown_count} kişi"})
        except Exception:
            pass
        cv2.imshow("Tanıma - Yoklama", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
    cap.release()
    cv2.destroyAllWindows()


def on_register():
    name = simpledialog.askstring("Kayıt", "İsim giriniz:")
    if not name:
        return
    student = simpledialog.askstring("Kayıt", "Öğrenci numarası giriniz:")
    if not student:
        return
    capture_and_save(name, student)


def on_recognize():
    recognizer, label_map = train_recognizer()
    if recognizer is None:
        return
    # Yoklama penceresi oluştur
    att_win = tk.Toplevel()
    att_win.title("Yoklama Listesi")
    vars_map = {}
    for label in sorted(label_map.keys()):
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(att_win, text=label_map[label], variable=var, state='disabled')
        cb.pack(anchor='w', padx=8, pady=2)
        vars_map[label] = var

    stop_event = threading.Event()
    worker = {"thread": None}

    def _start():
        if worker["thread"] and worker["thread"].is_alive():
            return
        stop_event.clear()
        # Bilinmeyen kişileri saymak için bir label ekle ve thread'e geçir
        unknown_label = tk.Label(att_win, text=f"{UNKNOWN_LABEL} : 0 kişi")
        unknown_label.pack(anchor='w', padx=8, pady=2)
        worker["unknown_label"] = unknown_label
        t = threading.Thread(target=_attendance_thread, args=(recognizer, label_map, vars_map, stop_event, att_win, unknown_label), daemon=True)
        worker["thread"] = t
        t.start()

    def _stop():
        stop_event.set()
        # Kaydı logla: tarih/saat, kaç kişi, isimler, bilinmeyen sayısı
        try:
            unknown_label = worker.get("unknown_label")
            unknown_count = 0
            if unknown_label is not None:
                txt = unknown_label.cget("text")
                m = re.search(r"(\d+)", txt)
                if m:
                    unknown_count = int(m.group(1))
            # Tanınan isimler
            present = [label_map[l] for l, v in vars_map.items() if v.get()]
            recognized_count = len(present)
            # Zaman damgası
            ts = datetime.datetime.now().isoformat()
            # CSV'ye yaz
            write_header = not os.path.exists(ATTENDANCE_LOG)
            with open(ATTENDANCE_LOG, "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(["timestamp", "recognized_count", "recognized_names", "unknown_count"])
                writer.writerow([ts, recognized_count, ";".join(present), unknown_count])
            # İnsan tarafından okunabilir metin dosyasına ekle (alt alta düzenli blok)
            try:
                with open(ATTENDANCE_LOG_TXT, "a", encoding='utf-8') as tf:
                    tf.write(f"Timestamp: {ts}\n")
                    tf.write(f"Recognized count: {recognized_count}\n")
                    tf.write("Recognized names:\n")
                    if present:
                        for p in present:
                            tf.write(f"- {p}\n")
                    else:
                        tf.write("- (none)\n")
                    tf.write(f"Unknown count: {unknown_count}\n")
                    tf.write("\n")
            except Exception:
                pass
        except Exception:
            pass

    btn_frame = tk.Frame(att_win)
    btn_frame.pack(pady=6)
    btn_start = tk.Button(btn_frame, text="Başlat", width=10, command=_start)
    btn_start.pack(side='left', padx=4)
    btn_stop = tk.Button(btn_frame, text="Durdur", width=10, command=_stop)
    btn_stop.pack(side='left', padx=4)
    btn_close = tk.Button(btn_frame, text="Kapat", width=10, command=lambda: ( _stop(), att_win.destroy()))
    btn_close.pack(side='left', padx=4)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Yüz Tanıma Sistemi")
    root.geometry("300x150")
    btn_register = tk.Button(root, text="1) Yüz Kaydet", width=20, command=on_register)
    btn_register.pack(pady=10)
    btn_recognize = tk.Button(root, text="2) Yüz Tanıma", width=20, command=on_recognize)
    btn_recognize.pack(pady=10)
    btn_exit = tk.Button(root, text="Çıkış", width=20, command=root.quit)
    btn_exit.pack(pady=5)
    root.mainloop()
