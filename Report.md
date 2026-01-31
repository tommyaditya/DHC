# LAPORAN PROYEK PENGOLAHAN CITRA DIGITAL
## HAND GESTURE CONTROL UNTUK CHROME DINO GAME

**Mata Kuliah:** Pengolahan Citra Digital (Semester 5)  
**Topik:** Penerapan MediaPipe Hand Tracking untuk Interaksi Manusia-Komputer (HCI)

---

## 1. PENDAHULUAN

### 1.1 Latar Belakang
Dalam perkembangan teknologi interaksi manusia dan komputer (*Human-Computer Interaction*), penggunaan keyboard dan mouse fisik mulai digantikan atau dilengkapi dengan kontrol berbasis gestur. Proyek ini bertujuan untuk mendemonstrasikan bagaimana teknologi *Computer Vision* dapat digunakan untuk mengontrol permainan sederhana tanpa sentuhan fisik, menggunakan webcam dan pengolahan citra digital.

### 1.2 Rumusan Masalah
Bagaimana cara mendeteksi gestur tangan (khususnya gerakan mencubit/pinch) secara real-time dan menerjemahkannya menjadi input keyboard (tombol Spasi) untuk mengontrol permainan?

### 1.3 Tujuan
1. Mengimplementasikan algoritma deteksi tangan menggunakan MediaPipe.
2. Menerapkan logika perhitungan jarak Euclidean pada titik landmark tangan.
3. Menciptakan antarmuka kontrol game "Chrome Dino" yang responsif.

---

## 2. LANDASAN TEORI

### 2.1 Pengolahan Citra Digital (Digital Image Processing)
Pengolahan citra digital adalah manipulasi gambar digital dengan algoritma komputer. Dalam proyek ini, teknik yang digunakan meliputi:
- **Image Acquisition**: Pengambilan frame video dari webcam.
- **Preprocessing**: Konversi ruang warna (Color Space Conversion) dari BGR ke RGB, serta pembalikan citra (*Horizontal Flip*).

### 2.2 MediaPipe Hands
MediaPipe adalah kerangka kerja *buka-sumber* dari Google. Modul **MediaPipe Hands** menggunakan *Machine Learning* untuk mendeteksi 21 titik referensi (*landmarks*) 3D pada tangan dari satu gambar saja, tanpa memerlukan perangkat keras kedalaman (*depth sensor*).

### 2.3 Deteksi Gestur (Pinch Detection)
Gestur "mencubit" dideteksi dengan mengukur jarak antara dua titik kunci:
- **Thumb Tip** (Ujung Jempol, Index 4)
- **Index Finger Tip** (Ujung Telunjuk, Index 8)

---

## 3. METODOLOGI

### 3.1 Alat dan Bahan
- **Bahasa Pemrograman**: Python 3.x
- **Library Utama**:
  - `opencv-python`: Pengolahan citra dan akses kamera.
  - `mediapipe`: Deteksi landmark tangan (menggunakan model `hand_landmarker.task`).
  - `pyautogui`: Simulasi penekanan tombol keyboard.

### 3.2 Alur Program (Flowchart)
1. **Inisialisasi**: Memuat model MediaPipe dan membuka Webcam.
2. **Loop Utama**:
   - Baca frame dari kamera.
   - *Flip* frame dan ubah warna ke RGB.
   - Deteksi tangan menggunakan MediaPipe.
   - Jika tangan terdeteksi:
     - Ambil koordinat ujung jempol (4) dan telunjuk (8).
     - Hitung jarak Euclidean antar kedua titik.
     - Jika Jarak < Threshold (Ambang Batas):
       - Tekan tombol **SPASI** (`pyautogui.keyDown`).
       - Visualisasikan garis penghubung dan teks "JUMP!".
     - Jika Jarak > Threshold:
       - Lepas tombol **SPASI** (`pyautogui.keyUp`).
   - Tampilkan frame ke layar.
3. **Selesai**: Jika tombol 'q' ditekan, tutup aplikasi.

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Struktur Kode
Proyek terdiri dari tiga file utama:
- `main.py`: Kode utama logika program.
- `requirements.txt`: Daftar dependensi library.
- `hand_landmarker.task`: Model data *machine learning*.

### 4.2 Analisis Algoritma (Code Snippet)
Bagian paling krusial adalah perhitungan jarak untuk menentukan aksi "Lompat":

```python
# Koordinat Jempol (4) dan Telunjuk (8)
thumb_tip = hand_landmarks[4]
index_tip = hand_landmarks[8]

# Perhitungan Jarak (Euclidean Distance pada titik ternormalisasi)
dist_normalized = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)

# Logika Threshold
PINCH_THRESHOLD = 0.05 
# 0.05 mewakili jarak relatif yang sangat dekat (sekitar 5% dari dimensi frame)

if dist_normalized < PINCH_THRESHOLD:
    # Aksi: Mencubit -> Lompat
    if not is_pinched:
        pyautogui.keyDown('space')
        is_pinched = True
else:
    # Aksi: Lepas -> Berhenti Lompat
    if is_pinched:
        pyautogui.keyUp('space')
        is_pinched = False
```

### 4.3 Optimasi Performa
- **Resolusi**: Kamera diatur ke 640x480 untuk menjaga FPS tetap tinggi namun cukup jelas untuk deteksi.
- **PyAutoGUI Pause**: Default delay 0.1 detik pada PyAutoGUI dinonaktifkan (`pyautogui.PAUSE = 0`) agar respon game instan tanpa lag.
- **Flip Image**: Gambar dibalik (`cv2.flip`) agar gerakan tangan pengguna terasa natural seperti bercermin.

---

## 5. KESIMPULAN
Proyek ini berhasil mengimplementasikan sistem kendali gestur tangan sederhana namun efektif. Dengan memanfaatkan efisiensi MediaPipe, sistem dapat berjalan secara *real-time* di CPU standar tanpa memerlukan GPU khusus. Deteksi gestur "pinch" terbukti menjadi metode yang intuitif untuk simulasi klik atau tombol spasi.

---

### CARA MENJALANKAN PROYEK
1. Pastikan Python terinstal.
2. Instal library: `pip install -r requirements.txt`
3. Jalankan program: `python main.py`
4. Buka Game Dino (chrome://dino) dan mainkan dengan gerakan tangan.
