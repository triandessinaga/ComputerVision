# 🔍 Smart Retail Inspector
### AI Computer Vision for Business — Praktikum Mandiri

[![Python](https://img.shields.io/badge/Python-3.10--3.12-blue?logo=python)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green?logo=opencv)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> **Mata Kuliah:** AI untuk Bisnis / Sistem Informasi  
> **Dosen:** Triandes Sinaga  
> **Durasi:** 150 menit praktikum + 120 menit tugas sawit  
> **Level:** Pemula — tidak perlu GPU, tidak perlu pengalaman AI

---

## 🎬 Apa yang Dibangun?

Aplikasi desktop **real-time** yang menggunakan kamera laptop untuk:
- Mendeteksi produk dengan AI (YOLO)
- Mencocokkan ke 20 produk nyata e-commerce Indonesia
- Mencatat ke keranjang belanja dengan konfirmasi operator
- Menghasilkan struk `.txt` + data `CSV` siap analisis

```
Webcam → YOLO AI → Produk Nyata → [SPACE] → Keranjang → [C] Checkout → Struk + CSV
```

---

## ⚡ Mulai dalam 5 Menit

```bash
# 1. Clone
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision

# 2. Virtual environment
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows PowerShell
# source .venv/bin/activate      # macOS/Linux

# 3. Install
pip install -r requirements.txt

# 4. Jalankan
python app.py
```

> Model YOLO (~50MB) diunduh otomatis saat pertama kali. Butuh internet sekali.

---

## ⌨️ Keyboard Shortcuts

| Tombol | Aksi |
|--------|------|
| `SPACE` | ✅ Tambah produk terdeteksi ke keranjang |
| `TAB` | 🔄 Ganti pilihan (jika > 1 objek terdeteksi) |
| `U` | ↩ Undo item terakhir |
| `C` | 💳 Checkout + kalkulator kembalian otomatis |
| `N` | 🔄 New / reset keranjang |
| `S` | 💾 Simpan inspeksi ke CSV (tanpa checkout) |
| `Q` / `Esc` | 🚪 Keluar |

---

## 📁 Struktur Proyek

```
ComputerVision/
│
├── app.py                    ← 🎯 File utama — jalankan ini
├── requirements.txt          ← 4 library yang dibutuhkan
├── .gitignore
│
├── data/
│   ├── catalog.json          ← 📦 20 produk real (edit harga di sini)
│   └── receipt_demo.png      ← Gambar struk untuk demo
│
├── output/                   ← 📊 Hasil runtime (tidak di-push ke GitHub)
│   ├── inspections.csv       ← Log inspeksi [S]
│   ├── transactions.csv      ← Log transaksi [C]
│   └── receipts/INV-*.txt    ← Struk per transaksi
│
├── tests/
│   └── test_business.py      ← 18 unit tests
│
└── docs/
    ├── PANDUAN_MAHASISWA.md  ← 📖 Panduan step-by-step 150 menit
    └── TUGAS_SAWIT.md        ← 🌴 Tugas transfer ke industri sawit
```

---

## 📦 Katalog — 20 Produk Real Indonesia

Setiap kelas YOLO dipetakan ke produk nyata yang ada di Tokopedia/Shopee/Alfamart:

| YOLO Class | Produk | Brand | Harga |
|------------|--------|-------|-------|
| `cell phone` | Samsung Galaxy A15 | Samsung | Rp 1.899.000 |
| `laptop` | ASUS VivoBook 14 Intel i3 | ASUS | Rp 5.499.000 |
| `keyboard` | Keyboard Logitech K120 USB | Logitech | Rp 175.000 |
| `mouse` | Mouse Wireless Logitech M170 | Logitech | Rp 149.000 |
| `bottle` | Aqua Botol Mineral 600ml | Aqua | Rp 4.500 |
| `cup` | Mie Sedaap Cup Ayam 75g | Wings Food | Rp 5.500 |
| `book` | Buku Tulis Sinar Dunia 58 Lbr | Sinar Dunia | Rp 7.500 |
| `scissors` | Gunting Joyko SC-809 | Joyko | Rp 18.500 |
| `banana` | Pisang Ambon (per 100g) | Lokal | Rp 3.000 |
| `apple` | Apel Fuji Import (per 100g) | Import | Rp 4.500 |
| `sandwich` | Roti Tawar Sari Roti Jumbo | Sari Roti | Rp 22.500 |
| `remote` | Remote TV Universal RM-L1268 | Universal | Rp 35.000 |
| + 8 lainnya | lihat `data/catalog.json` | | |

**Kelas yang diabaikan (blacklist):** `person`, `car`, `chair`, `cat`, `dog`, dan 49 kelas lain — tidak akan masuk keranjang meskipun terdeteksi di frame.

> Edit `data/catalog.json` untuk mengubah harga atau nama produk.

---

## 🔧 Mode Jalankan

```bash
python app.py                    # webcam default (index 0)
python app.py --camera 1         # webcam ke-2 / eksternal
python app.py --image foto.jpg   # gambar statis (tanpa webcam)
python app.py --conf 0.30        # turunkan threshold deteksi
```

---

## 🧪 Unit Tests

```bash
python -m unittest discover -s tests -v
```

```
test_all_have_required_fields ... ok
test_all_prices_positive ... ok
test_sum_equals_input ... ok
...
Ran 18 tests in 0.001s — OK
```

---

## 📊 Output Otomatis

### `output/transactions.csv` — dibuat saat checkout `[C]`
```
invoice,timestamp,kasir,sku,product,qty,unit_price,line_total,payment,change
INV-20261027-103500,2026-10-27T10:35:00,OPERATOR-01,MNM-001,
Aqua Botol Mineral 600ml,2,4500,9000,50000,41000
```
*Artinya: 2 botol × Rp 4.500 = Rp 9.000 | Bayar Rp 50.000 | Kembalian Rp 41.000*

### `output/inspections.csv` — dibuat saat tekan `[S]`
```
timestamp,sample_id,source,yolo_class,sku,product,category,price_idr,confidence,operator_confirmed
2026-10-27T10:30:00,ITEM-001,WEBCAM,bottle,MNM-001,Aqua Botol Mineral 600ml,Minuman,4500,0.876,YES
```

---

## 🌴 Tugas Sawit — Transfer ke Industri

Setelah praktikum retail, Anda ditantang menerapkan konsep yang sama ke **industri kelapa sawit**.

### Konteks Bisnis

> Perusahaan sawit di Sumatera ingin menggunakan AI untuk menggantikan
> inspeksi manual kualitas **Tandan Buah Segar (TBS)** di loading ramp.
> Saat ini grading dilakukan petugas — lambat, subjektif, tidak konsisten.

### Yang Perlu Anda Bandingkan

| Aspek | Smart Retail Inspector | SawitVision (Proposal Anda) |
|-------|----------------------|----------------------------|
| Objek | Botol, buku, ponsel | Tandan Buah Segar (TBS) |
| Model | Pretrained COCO (generik) | ? Custom atau pretrained? |
| Konfirmasi | Operator tekan SPACE | ? |
| Output | CSV transaksi + struk | ? |
| Lingkungan | Indoor, meja kasir | ? Loading ramp, outdoor |
| Skala | Puluhan item/hari | ? Ratusan ton/hari |

### Eksperimen Langsung

Cari 3 foto TBS dari internet (matang/mentah/sulit dinilai), lalu:

```bash
python app.py --image foto_tbs_matang.jpg
```

Catat apa yang terdeteksi. Model **tidak akan mengenali TBS** — dan itulah pelajarannya:

> Model generik tidak bisa dipakai untuk domain khusus.
> Butuh dataset berlabel dan fine-tuning untuk kasus spesifik.

### Skema Sistem yang Diusulkan

```
TBS di         ┌─────────┐   ┌──────────────┐   ┌─────────────────┐
Loading  ─────▶│ Kamera  │──▶│  YOLO Custom │──▶│ Petugas Validasi│
Ramp           │ IP/HD   │   │ (TBS Dataset)│   │ (Human-in-Loop) │
               └─────────┘   └──────────────┘   └────────┬────────┘
                                                          │ Konfirmasi
                                                          ▼
                                                  ┌───────────────┐
                                                  │   Database    │──▶ Dashboard QC
                                                  │  Inspeksi Log │    Manajer
                                                  └───────────────┘
```

### Yang Harus Anda Buat

Buat **proposal teknis** (1–2 halaman) berisi:

1. **Problem Statement** — kerugian bisnis jika grading TBS salah
2. **Proposed Solution** — spesifikasi kamera, jenis model, cara konfirmasi
3. **Data Requirements** — berapa foto TBS per kelas, siapa yang label
4. **Pilot KPI** — 3 metrik terukur (jangan mengarang target tanpa data)
5. **Risiko & Mitigasi** — min. 4 risiko
6. **Refleksi Etika** — hak pekerja, akuntabilitas, kepercayaan

📄 **Panduan lengkap:** [docs/TUGAS_SAWIT.md](docs/TUGAS_SAWIT.md)

---

## 🚧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Kamera hitam | Tutup Zoom/Teams · Settings → Privacy → Camera |
| Kamera tidak ditemukan | `python app.py --camera 1` |
| Tombol keyboard tidak respons | Klik area jendela GUI dulu, bukan terminal |
| FPS lambat | Normal di CPU — tutup aplikasi berat lain |
| Objek tidak terdeteksi | Tambah cahaya · jarak 30–60cm · `--conf 0.25` |
| Download model gagal | Cek koneksi internet (butuh sekali, ~50MB) |

---

## ⚠️ Disclaimer

Model YOLO pretrained COCO mengenali **kategori generik**, bukan merek/SKU spesifik.
Harga di `catalog.json` adalah **simulasi pendidikan**, bukan harga real.
Untuk kasir produksi: butuh model custom, barcode scanner, dan validasi sistem lengkap.

---

## 📚 Dokumentasi

| File | Isi |
|------|-----|
| [docs/PANDUAN_MAHASISWA.md](docs/PANDUAN_MAHASISWA.md) | Panduan step-by-step 150 menit |
| [docs/TUGAS_SAWIT.md](docs/TUGAS_SAWIT.md) | Tugas transfer industri sawit |

---

## 📝 Lisensi

MIT License — bebas digunakan untuk pendidikan.  
Model YOLO: [Ultralytics AGPL-3.0](https://github.com/ultralytics/ultralytics)

---

*AI untuk Bisnis — Sistem Informasi | © 2026 Triandes Sinaga*
