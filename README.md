# 🔍 Smart Retail Inspector
### AI Computer Vision for Business — Praktikum Mandiri

[![Python](https://img.shields.io/badge/Python-3.10--3.12-blue?logo=python)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Moodle](https://img.shields.io/badge/LMS-Moodle-purple)](https://moodle.org)

> **Mata Kuliah:** AI untuk Bisnis / Sistem Informasi  
> **Dosen:** Triandes Sinaga  
> **Durasi:** 150 menit mandiri + 120 menit tugas Sawit  
> **Level:** Pemula — tidak perlu GPU, tidak perlu pengalaman AI

---

## 🎬 Apa yang Akan Anda Buat?

Aplikasi desktop **real-time** yang menggunakan kamera laptop untuk mendeteksi produk, mencatat ke keranjang belanja, dan menghasilkan struk + data CSV — semua berjalan di laptop biasa tanpa internet setelah setup.

```
Webcam → YOLO AI → Produk Terdeteksi → [SPACE] → Keranjang → [C] Checkout → Struk + CSV
```

![Demo App](docs/assets/demo_screenshot.png)

---

## ⚡ Quick Start (5 Menit)

```bash
# 1. Clone repo
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision

# 2. Buat virtual environment
py -3 -m venv .venv

# 3. Aktifkan (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Jalankan!
python app.py
```

> Model YOLO (~50MB) diunduh otomatis saat pertama kali dijalankan.

---

## ⌨️ Keyboard Shortcuts

| Tombol | Fungsi |
|--------|--------|
| `SPACE` | ✅ Tambah produk terdeteksi ke keranjang |
| `TAB` | 🔄 Ganti pilihan deteksi (jika > 1 objek) |
| `U` | ↩ Undo item terakhir |
| `C` | 💳 Checkout + hitung kembalian |
| `N` | 🔄 New / reset keranjang |
| `S` | 💾 Simpan inspeksi ke CSV |
| `Q` / `Esc` | 🚪 Keluar |

---

## 📁 Struktur Proyek

```
ComputerVision/
│
├── app.py                   ← 🎯 Jalankan ini
├── requirements.txt         ← Dependencies
├── .gitignore
│
├── data/
│   ├── catalog.json         ← 📦 20 produk real (edit harga di sini)
│   └── receipt_demo.png     ← Demo OCR
│
├── output/                  ← 📊 Hasil otomatis (tidak di-push)
│   ├── inspections.csv      ← Log inspeksi [S]
│   ├── transactions.csv     ← Log transaksi [C]
│   └── receipts/            ← Struk .txt
│
├── tests/
│   └── test_business.py     ← 18 unit tests
│
└── docs/
    ├── PANDUAN_MAHASISWA.md ← 📖 Panduan lengkap step-by-step
    └── TUGAS_SAWIT.md       ← 🌴 Tugas transfer ke industri sawit
```

---

## 📦 Katalog Produk (20 Produk Real)

Semua produk dipetakan dari kelas YOLO COCO ke produk nyata e-commerce Indonesia:

| YOLO Class | Produk | Brand | Harga |
|------------|--------|-------|-------|
| `cell phone` | Samsung Galaxy A15 | Samsung | Rp 1.899.000 |
| `laptop` | ASUS VivoBook 14 | ASUS | Rp 5.499.000 |
| `keyboard` | Logitech K120 USB | Logitech | Rp 175.000 |
| `mouse` | Logitech M170 Wireless | Logitech | Rp 149.000 |
| `bottle` | Aqua Mineral 600ml | Aqua | Rp 4.500 |
| `book` | Buku Tulis Sinar Dunia | Sinar Dunia | Rp 7.500 |
| `banana` | Pisang Ambon (per 100g) | Segar | Rp 3.000 |
| `apple` | Apel Fuji Import (per 100g) | Import | Rp 4.500 |
| `scissors` | Gunting Joyko SC-809 | Joyko | Rp 18.500 |
| `sandwich` | Roti Tawar Sari Roti Jumbo | Sari Roti | Rp 22.500 |
| + 10 lainnya | lihat `data/catalog.json` | | |

> Edit `data/catalog.json` untuk mengganti harga atau nama produk.

---

## 🔧 Mode Alternatif

```bash
# Webcam ke-2
python app.py --camera 1

# Gambar statis (laptop tanpa webcam)
python app.py --image foto_produk.jpg

# Turunkan threshold deteksi
python app.py --conf 0.30
```

---

## 🧪 Unit Tests

```bash
python -m unittest discover -s tests -v
# Ran 18 tests ... OK
```

---

## 🚧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Kamera hitam | Tutup Zoom/Teams, cek Settings → Privacy → Camera |
| Kamera tidak ditemukan | `python app.py --camera 1` |
| Tombol tidak respons | Klik jendela utama GUI dulu |
| FPS lambat | Normal di CPU, tutup aplikasi berat lain |
| Objek tidak terdeteksi | Tambah cahaya, `--conf 0.25`, jarak 30–60cm |

---

## 📚 Dokumentasi Lengkap

- 📖 **[Panduan Mahasiswa](docs/PANDUAN_MAHASISWA.md)** — step-by-step 150 menit
- 🌴 **[Tugas Sawit](docs/TUGAS_SAWIT.md)** — transfer ke industri kelapa sawit
- 📋 **[Panduan Dosen](README_DOSEN.md)** — rubrik, narasi Moodle, tips fasilitasi

---

## ⚠️ Disclaimer Akademis

Model YOLO pretrained mengenali **kategori generik** (bottle, book, phone), bukan merek/SKU spesifik. Mapping harga di `catalog.json` adalah **simulasi demo pendidikan**, bukan data produk nyata. Untuk implementasi kasir produksi diperlukan training model khusus, integrasi barcode, dan validasi sistem yang komprehensif.

---

## 📝 Lisensi

MIT License — bebas digunakan untuk keperluan pendidikan.  
Model YOLO: [Ultralytics AGPL-3.0](https://github.com/ultralytics/ultralytics)

---

*Praktikum AI untuk Bisnis — Sistem Informasi | © 2026 Triandes Sinaga*
