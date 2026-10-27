# 📚 Smart Retail Inspector — Paket Pengajar

> **Untuk dosen / fasilitator** — rubrik, narasi Moodle, dan tips fasilitasi.  
> Mahasiswa cukup baca `README.md` dan `docs/PANDUAN_MAHASISWA.md`.

---

## 📋 Info Kelas

| Item | Detail |
|------|--------|
| Mata Kuliah | AI untuk Bisnis / Pengantar Sistem Informasi |
| Sub-CPMK | 3.1 — Computer Vision untuk Analisis Bisnis |
| Mode | Mandiri / Asynchronous / Lab terbimbing |
| Durasi | 150 menit (+ 120 menit mandiri lanjutan) |
| Prasyarat | Python dasar, konsep basis data |
| Kelompok | Individual atau maks. 2 mahasiswa |

---

## 📢 Narasi untuk Moodle / LMS

```
Halo Mahasiswa! 👋

Pada pertemuan ini, Anda akan membangun prototipe AI Vision
untuk retail menggunakan Python, OpenCV, dan YOLO.

Bayangkan Anda junior analyst di sebuah toko:
Tugas Anda membuat sistem yang membantu petugas mengenali 
produk lewat kamera — lebih cepat dari scan manual,
tapi tetap membutuhkan verifikasi manusia.

📦 Apa yang Anda bangun:
  ✓ Aplikasi GUI desktop real-time
  ✓ Deteksi objek dengan AI (YOLO)
  ✓ Keranjang belanja + checkout + kembalian
  ✓ Pencatatan data ke CSV (siap dianalisis Excel/Python)

🎮 Ada game-based challenge dengan XP points!

📌 Mulai dari: docs/PANDUAN_MAHASISWA.md
📌 Tidak perlu GPU atau API berbayar
📌 Bisa dikerjakan dengan laptop biasa

Selamat mencoba! 🚀
```

---

## 🗓️ Alokasi Waktu 150 Menit

| Waktu | Aktivitas | Output |
|-------|-----------|--------|
| 0–10' | Briefing & cerita konteks bisnis | — |
| 10–25' | Setup environment + install | Screenshot terminal OK |
| 25–45' | Jalankan aplikasi, pahami konsep CV | Webcam aktif, bbox terlihat |
| 45–75' | Eksperimen 6 kondisi berbeda | Tabel uji lengkap |
| 75–105' | Edit katalog, keranjang, checkout | 1 struk + CSV tersimpan |
| 105–125' | Business Studio: diagram sistem | Diagram alur |
| 125–140' | Privacy Detective + refleksi | Jawaban 4 pertanyaan |
| 140–150' | Demo singkat + Q&A | Presentasi 2 menit |

---

## 🏆 Rubrik Penilaian (100 Poin)

### Komponen 1 — Setup & Deteksi Real-time (25 poin)

| Kriteria | Bobot | Indikator |
|----------|-------|-----------|
| Instalasi berhasil | 5 | Screenshot terminal, semua library terinstall |
| Webcam + bounding box aktif | 10 | Screenshot/video GUI dengan bbox |
| Memahami confidence score | 5 | Jawaban tertulis: apa arti conf:0.8? |
| Memahami keterbatasan model | 5 | Contoh kasus model salah + penjelasan |

### Komponen 2 — Eksperimen & Analisis (25 poin)

| Kriteria | Bobot | Indikator |
|----------|-------|-----------|
| Tabel 6+ eksperimen terdokumentasi | 15 | Kondisi berbeda: cahaya, jarak, sudut |
| Hitung success rate | 5 | Formula: benar/total × 100% |
| Identifikasi faktor pengaruh | 5 | Min. 2 faktor + penjelasan |

### Komponen 3 — Integrasi Bisnis (25 poin)

| Kriteria | Bobot | Indikator |
|----------|-------|-----------|
| Edit catalog.json | 5 | Harga diubah, screenshot sebelum/sesudah |
| Keranjang + checkout berjalan | 10 | Screenshot dialog checkout + kembalian |
| CSV tersimpan & valid | 5 | Screenshot Excel/LibreOffice buka CSV |
| Struk tersimpan | 5 | Isi struk .txt yang benar |

### Komponen 4 — Analisis Bisnis & Etika (15 poin)

| Kriteria | Bobot | Indikator |
|----------|-------|-----------|
| Diagram alur sistem | 5 | Minimal: Kamera → AI → Validasi → DB → Dashboard |
| Privacy Detective | 5 | Jawaban 5 skenario dengan alasan |
| Refleksi kritis | 5 | 4 pertanyaan dijawab dengan substansi |

### Komponen 5 — Dokumentasi & Presentasi (10 poin)

| Kriteria | Bobot | Indikator |
|----------|-------|-----------|
| README/laporan rapi | 5 | Struktur jelas, screenshot relevan |
| Demo 2 menit | 5 | Menunjukkan fitur utama, bisa menjawab pertanyaan |

---

## 💡 Pertanyaan Diskusi untuk Kelas

**Konseptual:**
1. Mengapa kita tidak bisa langsung pakai model ini untuk kasir nyata?
2. Apa bedanya `confidence: 0.9` vs `confidence: 0.4`?
3. Jika botol Aqua dan botol Sprite sama-sama terdeteksi `bottle`, masalah apa yang timbul?

**Bisnis:**
4. Data apa yang paling berharga dari `inspections.csv` untuk manajer toko?
5. Berapa ROI jika sistem ini mengurangi waktu kasir 30 detik per transaksi?
6. Apa risiko jika sistem salah deteksi produk mahal sebagai produk murah?

**Teknis:**
7. Mengapa threading dibutuhkan untuk aplikasi kamera real-time?
8. Apa yang terjadi jika threshold confidence terlalu rendah? Terlalu tinggi?

---

## 🔬 Roadmap ke Produksi Nyata

```
DEMO (hari ini)
    │
    ▼
PILOT (2-4 minggu)
  ├── Dataset foto produk berlabel (500+ foto/SKU)
  ├── Fine-tuning YOLO dengan produk aktual
  ├── Database SQLite → PostgreSQL
  ├── Barcode scanner sebagai fallback wajib
  └── Login kasir + audit trail
    │
    ▼
PRODUCTION
  ├── Integrasi ERP/POS (SAP, Moka, dll)
  ├── Real-time inventory update
  ├── Role-based access control
  ├── Model monitoring & retraining pipeline
  ├── GDPR/UU PDP compliance
  └── SLA uptime + disaster recovery
```

**KPI yang harus ditetapkan sebelum go-live:**
- Akurasi deteksi per kategori produk > threshold bisnis
- Waktu deteksi < X detik
- Tingkat false positive (produk mahal salah terdeteksi murah)
- Tingkat override operator
- Uptime sistem

---

## ⚠️ Catatan Penting untuk Dosen

### Manajemen Ekspektasi

> **Sampaikan sejak awal:** YOLO pretrained mengenali *kategori generik*,
> bukan merek. `bottle` bisa Aqua, bisa Sprite, bisa botol parfum.
> Sistem ini adalah **prototipe pendidikan**, bukan solusi kasir siap pakai.

### Tips Fasilitasi

1. **Kelas tanpa webcam:** gunakan `python app.py --image foto.jpg`  
   Siapkan 3-4 foto produk sebagai fallback.

2. **Internet lambat:** unduh `yolo11n.pt` sebelum kelas dan taruh di folder proyek.
   ```
   https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
   ```

3. **Laptop lambat:** `yolo11n` sudah yang paling ringan. FPS 5-10 masih bisa dipakai.

4. **Mahasiswa ingin menambah produk:** cukup edit `catalog.json`, tidak perlu training ulang.
   Tapi jelaskan: kalau produk tidak ada di COCO (misal TBS sawit), model tidak akan deteksi.

### Privasi & Etika

- Ingatkan: kamera tidak boleh diarahkan ke wajah orang tanpa izin
- Jangan simpan foto yang ada orang di dalamnya dalam output/
- Semua data berjalan lokal — tidak ada upload ke server

---

## 📦 Checklist Persiapan Kelas

```
□ Python 3.10–3.12 terinstall di semua laptop
□ pip berfungsi (py --version dan pip --version)
□ yolo11n.pt sudah diunduh (opsional, bisa otomatis)
□ Webcam laptop berfungsi (tes dengan kamera bawaan OS)
□ Ada benda: botol, buku, gelas, ponsel (1 set cukup)
□ VS Code terinstall dengan Python extension
□ Koneksi internet (minimal untuk unduh model pertama kali)
```

---

*Pertanyaan? Buka GitHub Issues atau hubungi via email dosen.*
