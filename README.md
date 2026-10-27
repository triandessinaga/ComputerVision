# 🔍 Smart Retail Inspector
### AI Computer Vision for Business — Praktikum Mandiri

[![Python](https://img.shields.io/badge/Python-3.10--3.12-blue?logo=python)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics%2011-orange)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> **Mata Kuliah:** AI untuk Bisnis / Sistem Informasi
> **Dosen:** Triandes Sinaga
> **Durasi:** 150 menit praktikum + 120 menit tugas sawit
> **Level:** Pemula — tidak perlu GPU, tidak perlu pengalaman AI sebelumnya

---

## 🎯 Apa yang Akan Dibangun?

Aplikasi desktop **real-time** yang menggunakan kamera laptop untuk:

- Mendeteksi produk dengan AI (YOLO) — **tanpa training ulang**
- Mencocokkan hasil deteksi ke **20 produk nyata** e-commerce Indonesia
- Mencatat ke keranjang belanja dengan **konfirmasi operator**
- Menghasilkan **struk `.txt`** dan **data CSV** siap analisis di Excel

```
Webcam → YOLO AI → Produk Terdeteksi → [SPACE] konfirmasi
       → Keranjang → [C] Checkout → Struk + CSV
```

---

## 📋 Daftar Isi

1. [Persiapan Sistem](#1-persiapan-sistem)
2. [Bangun dari Nol — Windows](#2-bangun-dari-nol--windows)
3. [Bangun dari Nol — macOS](#3-bangun-dari-nol--macos)
4. [Clone dari GitHub (Alternatif Cepat)](#4-clone-dari-github--alternatif-cepat)
5. [Keyboard Shortcuts](#5-keyboard-shortcuts)
6. [Katalog Produk](#6-katalog-produk)
7. [Panduan Praktikum](#7-panduan-praktikum)
8. [Tugas Sawit](#8-tugas-sawit)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Persiapan Sistem

### Yang Dibutuhkan

| Kebutuhan | Spesifikasi Minimum |
|-----------|-------------------|
| OS | Windows 10/11 atau macOS 12+ |
| Python | Versi 3.10, 3.11, atau 3.12 |
| RAM | 4 GB (8 GB lebih baik) |
| Disk | 2 GB ruang kosong |
| Webcam | Kamera bawaan laptop sudah cukup |
| Internet | Dibutuhkan sekali saat setup (~300MB download) |

### Yang Perlu Diinstall

- **Python 3.10–3.12** — bahasa pemrograman
- **VS Code** — editor kode (bisa pakai editor lain)
- **Library Python** — diinstall otomatis via `pip`
- **Model YOLO** — diunduh otomatis saat pertama jalan

---

## 2. Bangun dari Nol — Windows

> Ikuti langkah ini jika pakai **Windows 10 atau Windows 11**.
> Semua perintah dijalankan di **PowerShell** atau **Command Prompt**.

---

### 2.1 Install Python

**Cek dulu apakah Python sudah ada:**

Buka **PowerShell** (tekan `Windows+R` → ketik `powershell` → Enter):
```
py --version
```

Jika muncul `Python 3.10.x` atau lebih baru → **lanjut ke 2.2**.

**Jika belum ada atau versi lama:**

1. Buka browser → pergi ke **https://python.org/downloads**
2. Klik tombol biru besar **"Download Python 3.12.x"**
3. Buka file `.exe` yang sudah diunduh
4. ⚠️ **WAJIB centang kotak "Add Python to PATH"** di bagian paling bawah halaman pertama installer
5. Klik **"Install Now"**
6. Tunggu hingga muncul pesan "Setup was successful"
7. Klik **Close**
8. **Tutup** PowerShell lama → **buka PowerShell baru**
9. Ketik lagi: `py --version` → harus muncul versinya

---

### 2.2 Install VS Code

1. Buka **https://code.visualstudio.com/download**
2. Klik **"Windows"** → unduh file `.exe`
3. Jalankan installer → klik **Next** terus → klik **Install** → **Finish**
4. Buka VS Code
5. Tekan `Ctrl+Shift+X` → cari **Python** → pilih ekstensi dari **Microsoft** → klik **Install**

---

### 2.3 Buat Folder Proyek

1. Buka **File Explorer** (`Windows+E`)
2. Navigasi ke lokasi yang mudah diingat, contoh: `C:\Users\NamaAnda\Documents`
3. Klik kanan di area kosong → **New** → **Folder**
4. Beri nama: `SmartRetail`

**Buka folder di VS Code:**
1. Buka VS Code
2. Klik `File` → `Open Folder`
3. Pilih folder `SmartRetail` → klik **Select Folder**
4. Buka terminal: klik `Terminal` → `New Terminal`

---

### 2.4 Buat Virtual Environment

Di terminal VS Code (pastikan Anda berada di dalam folder `SmartRetail`):
```
py -3 -m venv .venv
```

Folder `.venv` akan muncul di panel kiri VS Code.

**Aktifkan virtual environment:**
```
.\.venv\Scripts\Activate.ps1
```

Jika muncul error **"execution of scripts is disabled"**:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Ketik `Y` → tekan Enter → coba aktifkan lagi.

**Alternatif menggunakan CMD:**
```
.venv\Scripts\activate.bat
```

✅ **Berhasil** jika terminal berubah menjadi:
```
(.venv) PS C:\Users\NamaAnda\Documents\SmartRetail>
```

---

### 2.5 Buat File `requirements.txt`

Di VS Code, klik ikon **New File** (atas panel Explorer kiri) → ketik `requirements.txt` → Enter.

Isi file dengan teks berikut:
```
ultralytics>=8.3,<9
opencv-python>=4.8,<5
Pillow>=10,<13
pytesseract>=0.3.10,<1
```

Simpan dengan `Ctrl+S`.

---

### 2.6 Install Dependencies

Di terminal (pastikan ada tanda `(.venv)`):
```
pip install -r requirements.txt
```

Proses ini mengunduh dan menginstall 4 library utama:

| Library | Fungsi |
|---------|--------|
| `ultralytics` | Model AI YOLO untuk deteksi objek |
| `opencv-python` | Baca webcam dan proses gambar |
| `Pillow` | Tampilkan frame kamera di GUI Tkinter |
| `pytesseract` | OCR (baca teks dari gambar, opsional) |

Tunggu **5–10 menit**. Selesai jika muncul:
```
Successfully installed ultralytics-X.X opencv-python-X.X ...
```

> Jika muncul error **"Microsoft Visual C++ 14.0 required"**:
> Download **Build Tools** di https://visualstudio.microsoft.com/visual-cpp-build-tools/
> Centang **"C++ build tools"** → Install → ulangi `pip install`.

---

### 2.7 Buat Struktur Folder

Di terminal:
```
mkdir data, output, tests
```

---

### 2.8 Buat `data\catalog.json`

Di VS Code: klik folder `data` → ikon **New File** → ketik `catalog.json` → Enter.

Salin seluruh teks JSON di bawah ini dan tempel ke file tersebut, lalu simpan `Ctrl+S`:

```json
{
  "_comment": "Mapping YOLO class (COCO dataset) ke produk nyata e-commerce Indonesia",

  "bottle":     {"sku":"MNM-001","product":"Aqua Botol Mineral 600ml",        "brand":"Aqua",       "price_idr":4500,    "category":"Minuman"},
  "cup":        {"sku":"MNM-002","product":"Mie Sedaap Cup Ayam 75g",          "brand":"Wings Food", "price_idr":5500,    "category":"Makanan Instan"},
  "book":       {"sku":"ATK-001","product":"Buku Tulis Sinar Dunia 58 Lembar", "brand":"Sinar Dunia","price_idr":7500,    "category":"Alat Tulis"},
  "cell phone": {"sku":"ELK-001","product":"Samsung Galaxy A15",               "brand":"Samsung",    "price_idr":1899000, "category":"Smartphone"},
  "laptop":     {"sku":"ELK-002","product":"ASUS VivoBook 14 Intel i3",        "brand":"ASUS",       "price_idr":5499000, "category":"Laptop"},
  "keyboard":   {"sku":"ELK-003","product":"Keyboard Logitech K120 USB",       "brand":"Logitech",   "price_idr":175000,  "category":"Aksesoris Komputer"},
  "mouse":      {"sku":"ELK-004","product":"Mouse Wireless Logitech M170",     "brand":"Logitech",   "price_idr":149000,  "category":"Aksesoris Komputer"},
  "scissors":   {"sku":"ATK-002","product":"Gunting Joyko SC-809",             "brand":"Joyko",      "price_idr":18500,   "category":"Alat Tulis"},
  "banana":     {"sku":"BSY-001","product":"Pisang Ambon Lokal (per 100g)",    "brand":"Lokal",      "price_idr":3000,    "category":"Buah & Sayur"},
  "apple":      {"sku":"BSY-002","product":"Apel Fuji Import (per 100g)",      "brand":"Import",     "price_idr":4500,    "category":"Buah & Sayur"},
  "orange":     {"sku":"BSY-003","product":"Jeruk Medan Manis (per 100g)",     "brand":"Lokal",      "price_idr":3500,    "category":"Buah & Sayur"},
  "carrot":     {"sku":"BSY-004","product":"Wortel Segar Kupas (per 100g)",    "brand":"Lokal",      "price_idr":2000,    "category":"Buah & Sayur"},
  "remote":     {"sku":"ELK-005","product":"Remote TV Universal RM-L1268",     "brand":"Universal",  "price_idr":35000,   "category":"Elektronik"},
  "clock":      {"sku":"ELK-006","product":"Jam Dinding Deli 12 Inch",         "brand":"Deli",       "price_idr":89000,   "category":"Elektronik"},
  "bowl":       {"sku":"RMH-001","product":"Mangkok Melamin Lion Star 15cm",   "brand":"Lion Star",  "price_idr":12000,   "category":"Peralatan Dapur"},
  "sandwich":   {"sku":"MKN-001","product":"Roti Tawar Sari Roti Jumbo 650g",  "brand":"Sari Roti",  "price_idr":22500,   "category":"Makanan"},
  "pizza":      {"sku":"MKN-002","product":"Frozen Pizza Belfoods Royal 135g", "brand":"Belfoods",   "price_idr":35000,   "category":"Makanan Beku"},
  "cake":       {"sku":"MKN-003","product":"Bolu Gulung Nabati Richeese",      "brand":"Nabati",     "price_idr":18000,   "category":"Snack"},
  "vase":       {"sku":"RMH-002","product":"Vas Bunga Keramik Dekorasi",       "brand":"Ikea",       "price_idr":79000,   "category":"Dekorasi"},
  "fork":       {"sku":"RMH-003","product":"Garpu Makan Stainless Steel 6pcs", "brand":"Zebra",      "price_idr":32000,   "category":"Peralatan Dapur"}
}
```

---

### 2.9 Unduh `app.py` dan File Test

Di terminal PowerShell:
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/app.py" -OutFile "app.py"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/tests/test_business.py" -OutFile "tests\test_business.py"
```

**Jika perintah di atas gagal (cara manual):**
1. Buka https://github.com/triandessinaga/ComputerVision
2. Klik file `app.py` → klik tombol **Raw** (pojok kanan atas)
3. `Ctrl+A` → `Ctrl+C` (copy semua)
4. Di VS Code buat file `app.py` → `Ctrl+V` → `Ctrl+S`
5. Ulangi untuk `tests/test_business.py`

---

### 2.10 Verifikasi dan Jalankan

**Verifikasi instalasi:**
```
python -m unittest discover -s tests -v
```

Harus muncul: `Ran 18 tests in 0.001s — OK`

**Jalankan aplikasi:**
```
python app.py
```

Model YOLO (~50MB) diunduh otomatis pertama kali. Tunggu jendela GUI terbuka.

> Jika kamera tidak terbuka: **Settings** → **Privacy & Security** → **Camera**
> → aktifkan **"Let desktop apps access your camera"**

---

## 3. Bangun dari Nol — macOS

> Ikuti langkah ini jika pakai **macOS Monterey (12) atau lebih baru**.
> Semua perintah dijalankan di **Terminal**.
> Buka Terminal: tekan `Cmd+Space` → ketik `Terminal` → Enter.

---

### 3.1 Install Python

**Cek dulu apakah Python sudah ada:**
```bash
python3 --version
```

Jika muncul `Python 3.10.x` atau lebih baru → **lanjut ke 3.2**.

**Install via Homebrew (direkomendasikan):**
```bash
# Langkah 1: Install Homebrew (package manager macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ikuti instruksi di layar, masukkan password Mac jika diminta

# Langkah 2: Install Python
brew install python@3.12

# Langkah 3: Verifikasi
python3 --version
```

**Install via installer langsung (tanpa Homebrew):**
1. Buka **https://python.org/downloads/macos**
2. Download **"macOS 64-bit universal2 installer"** untuk Python 3.12
3. Buka file `.pkg` → ikuti wizard → klik **Continue** dan **Install**
4. Buka Terminal baru → ketik `python3 --version`

---

### 3.2 Install VS Code

1. Buka **https://code.visualstudio.com/download**
2. Klik **"Mac"** → unduh file `.zip`
3. Buka file `.zip` → drag **Visual Studio Code.app** ke folder **Applications**
4. Buka VS Code dari **Applications** atau Spotlight (`Cmd+Space` → ketik `Code`)
5. Tekan `Cmd+Shift+X` → cari **Python** → pilih dari **Microsoft** → **Install**

**Tambahkan VS Code ke PATH** (agar bisa buka dari terminal):
1. Di VS Code tekan `Cmd+Shift+P`
2. Ketik: `Shell Command: Install 'code' command in PATH`
3. Tekan Enter

---

### 3.3 Buat Folder Proyek

Di Terminal:
```bash
# Buat folder di Documents
mkdir -p ~/Documents/SmartRetail

# Masuk ke folder
cd ~/Documents/SmartRetail

# Buka di VS Code
code .
```

Atau cara manual:
1. Buka **Finder** → navigasi ke **Documents**
2. `Cmd+Shift+N` → buat folder baru → beri nama `SmartRetail`
3. Di VS Code: `File` → `Open Folder` → pilih `SmartRetail`

---

### 3.4 Buat Virtual Environment

Di terminal VS Code (menu `Terminal` → `New Terminal`):
```bash
python3 -m venv .venv
```

**Aktifkan virtual environment:**
```bash
source .venv/bin/activate
```

✅ **Berhasil** jika terminal berubah menjadi:
```
(.venv) nama@MacBook SmartRetail %
```

> ⚠️ Setiap kali membuka terminal baru, jalankan lagi `source .venv/bin/activate`

---

### 3.5 Buat File `requirements.txt`

Di VS Code: klik ikon **New File** → ketik `requirements.txt` → Enter.

Isi:
```
ultralytics>=8.3,<9
opencv-python>=4.8,<5
Pillow>=10,<13
pytesseract>=0.3.10,<1
```

Simpan dengan `Cmd+S`.

---

### 3.6 Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu **5–10 menit**.

> Jika muncul error **"error: command 'gcc' failed"** atau **"Xcode required"**:
> ```bash
> xcode-select --install
> ```
> Klik **Install** di dialog yang muncul → tunggu selesai (~15 menit) → ulangi `pip install`.

---

### 3.7 Buat Struktur Folder

```bash
mkdir -p data output tests
```

---

### 3.8 Buat `data/catalog.json`

Di VS Code: klik folder `data` → **New File** → `catalog.json`.

Salin isi JSON yang sama seperti di **bagian 2.8** di atas → `Cmd+V` → `Cmd+S`.

---

### 3.9 Unduh `app.py` dan File Test

```bash
curl -o app.py https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/app.py

curl -o tests/test_business.py https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/tests/test_business.py
```

**Jika curl gagal (cara manual):**
Sama seperti di bagian 2.9, buka GitHub → Raw → `Cmd+A` → `Cmd+C` → paste ke VS Code.

---

### 3.10 Verifikasi dan Jalankan

**Verifikasi:**
```bash
python3 -m unittest discover -s tests -v
```

Harus muncul: `Ran 18 tests in 0.001s — OK`

**Jalankan:**
```bash
python3 app.py
```

> **Kamera tidak terbuka di macOS?**
> Buka **System Settings** → **Privacy & Security** → **Camera**
> → aktifkan izin untuk **Terminal** dan/atau **Python**
> → tutup dan buka ulang Terminal → jalankan lagi

---

## 4. Clone dari GitHub — Alternatif Cepat

> Gunakan cara ini jika:
> - Waktu terbatas dan ingin langsung mencoba
> - Ada kendala teknis saat bangun dari nol
> - Ingin memastikan kode yang dipakai sama persis dengan repositori resmi

### Install Git

**🪟 Windows:** Download di https://git-scm.com/download/win → install dengan pengaturan default

**🍎 macOS:** Git biasanya sudah tersedia. Cek: `git --version`
Jika belum: `brew install git` atau `xcode-select --install`

---

### Clone dan Setup

**🪟 Windows (PowerShell):**
```powershell
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```

**🍎 macOS / Linux:**
```bash
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 app.py
```

### Perbandingan: Bangun Sendiri vs Clone

| Aspek | Bangun dari Nol | Clone dari GitHub |
|-------|----------------|-------------------|
| Waktu setup | 30–45 menit | 10–15 menit |
| Pemahaman kode | ✅ Lebih dalam | Langsung jalan |
| Risiko typo | Ada (perlu teliti) | Tidak ada |
| Cocok untuk | Belajar mendalam | Demo cepat |

> 💡 Apapun caranya, semua eksperimen dan tugas sawit tetap harus dikerjakan sendiri.

---

## 5. Keyboard Shortcuts

Setelah aplikasi terbuka, shortcut ini aktif **selama jendela GUI dalam fokus**
(klik area jendela aplikasi dulu sebelum menekan tombol):

| Tombol | Aksi | Kapan Dipakai |
|--------|------|---------------|
| `SPACE` | ✅ Tambah produk terdeteksi ke keranjang | Saat kamera aktif & objek terdeteksi |
| `TAB` | 🔄 Ganti ke deteksi berikutnya | Jika ada > 1 objek di frame |
| `U` | ↩ Undo — hapus item terakhir dari keranjang | Jika salah tambah |
| `C` | 💳 Buka dialog Checkout + kembalian | Saat keranjang sudah terisi |
| `N` | 🔄 Reset — kosongkan keranjang | Mulai transaksi baru |
| `S` | 💾 Simpan inspeksi ke CSV | Untuk mencatat tanpa checkout |
| `Q` | 🚪 Keluar dari aplikasi | — |
| `Esc` | 🚪 Keluar dari aplikasi | — |

---

## 6. Katalog Produk

20 produk dipetakan dari kelas YOLO COCO ke produk nyata yang tersedia di Tokopedia, Shopee, dan Alfamart/Indomaret:

| YOLO Class | Produk | Brand | Harga |
|------------|--------|-------|-------|
| `cell phone` | Samsung Galaxy A15 | Samsung | Rp 1.899.000 |
| `laptop` | ASUS VivoBook 14 Intel i3 | ASUS | Rp 5.499.000 |
| `keyboard` | Keyboard Logitech K120 USB | Logitech | Rp 175.000 |
| `mouse` | Mouse Wireless Logitech M170 | Logitech | Rp 149.000 |
| `bottle` | Aqua Botol Mineral 600ml | Aqua | Rp 4.500 |
| `cup` | Mie Sedaap Cup Ayam Spesial 75g | Wings Food | Rp 5.500 |
| `book` | Buku Tulis Sinar Dunia 58 Lembar | Sinar Dunia | Rp 7.500 |
| `scissors` | Gunting Joyko SC-809 All Purpose | Joyko | Rp 18.500 |
| `banana` | Pisang Ambon Lokal (per 100g) | Lokal | Rp 3.000 |
| `apple` | Apel Fuji Import (per 100g) | Import | Rp 4.500 |
| `orange` | Jeruk Medan Manis (per 100g) | Lokal | Rp 3.500 |
| `carrot` | Wortel Segar Kupas (per 100g) | Lokal | Rp 2.000 |
| `remote` | Remote TV Universal RM-L1268 | Universal | Rp 35.000 |
| `clock` | Jam Dinding Deli 12 Inch | Deli | Rp 89.000 |
| `bowl` | Mangkok Melamin Lion Star 15cm | Lion Star | Rp 12.000 |
| `sandwich` | Roti Tawar Sari Roti Jumbo 650g | Sari Roti | Rp 22.500 |
| `pizza` | Frozen Pizza Belfoods Royal 135g | Belfoods | Rp 35.000 |
| `cake` | Bolu Gulung Nabati Richeese | Nabati | Rp 18.000 |
| `vase` | Vas Bunga Keramik Dekorasi | Ikea | Rp 79.000 |
| `fork` | Garpu Makan Stainless Steel 6pcs | Zebra | Rp 32.000 |

**Kelas yang diabaikan secara otomatis:**
`person`, `car`, `bicycle`, `chair`, `couch`, `dog`, `cat`, dan 47 kelas lain
dari COCO dataset — tidak akan masuk keranjang meski terdeteksi di frame.

**Edit harga atau nama produk:**
Buka `data/catalog.json` → ubah nilai `price_idr` atau `product` → simpan → jalankan ulang.

---

## 7. Panduan Praktikum

### 7.1 Cara Kerja Sistem

```
┌──────────┐    ┌───────────────────┐    ┌─────────────────────────┐
│  Webcam  │───▶│   YOLO Model      │───▶│    catalog.json         │
│  Laptop  │    │  (AI Detection)   │    │  (Business Mapping)     │
└──────────┘    └───────────────────┘    └─────────────────────────┘
                        │                           │
                  "bottle" 0.87          "Aqua 600ml — Rp 4.500"
                        │                      Brand: Aqua
                        │
                 SPACE ← Operator konfirmasi
                        │
             ┌──────────▼──────────┐
             │     Keranjang       │──▶ [C] Checkout ──▶ CSV + Struk
             └─────────────────────┘
```

### Kosakata Penting

| Istilah | Artinya |
|---------|---------|
| **Frame** | 1 foto dari video (30 foto/detik = 30 FPS) |
| **Bounding Box** | Kotak yang mengelilingi objek yang terdeteksi |
| **YOLO Class** | Nama kategori objek: `bottle`, `book`, `person`, dll |
| **Confidence** | Skor keyakinan AI: `0.87` artinya 87% yakin |
| **COCO** | Dataset 80 kategori benda yang dipakai melatih model YOLO |
| **Blacklist** | Kelas yang sengaja diabaikan agar tidak masuk keranjang |

### ⚠️ Batasan yang Wajib Dipahami

> Model YOLO ini mengenali **kategori generik**, bukan merek spesifik.
> `cell phone` bisa Samsung, iPhone, atau Xiaomi — AI tidak bisa membedakan.
> Itulah mengapa operator **wajib menekan SPACE** sebagai konfirmasi sebelum data masuk.
> Sistem ini adalah **prototipe pendidikan**, bukan kasir produksi.

---

### 7.2 Tahap A — Kenali Aplikasi (0–20 menit)

**Layout GUI:**
```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 Smart Retail Inspector          👤 OPERATOR-01   🕐 Waktu    │
├───────────────────────────┬──────────────────────────────────────┤
│  📷 AI Kamera  │📋 Katalog │       🛒 Keranjang Belanja           │
│  ┌─────────────┐ 🎥Kontrol │  Produk     Qty   Harga   Subtotal  │
│  │             │ ──────── │  ─────────────────────────────────  │
│  │  KAMERA     │ ▶Aktifkan │                                     │
│  │  LIVE (16:9)│ ■ Stop   │                                     │
│  │             │ ──────── │  Total:               Rp 0          │
│  └─────────────┘ 🎯Deteksi│  [💳 CHECKOUT  [C]]                  │
│  ✅ Feedback     ⌨Shortcut │  [🔄 Reset     [N]]                  │
└───────────────────────────┴──────────────────────────────────────┘
```

**Langkah pertama:**
1. Klik tab **📷 AI Kamera**
2. Klik tombol **▶ Aktifkan Kamera** (di panel kanan kamera)
3. Arahkan **botol air** ke webcam — jarak ideal 30–60 cm, cahaya cukup
4. Panel **🎯 Deteksi Sekarang** akan menampilkan nama produk + confidence
5. Tekan `SPACE` → produk masuk keranjang kanan
6. Tekan `C` → dialog checkout terbuka dengan kembalian otomatis

📸 **Checkpoint A:** Screenshot GUI dengan bounding box aktif dan 1 produk di keranjang.

---

### 7.3 Tahap B — Eksperimen (20–70 menit)

**Tabel eksperimen — isi minimal 6 baris:**

| # | Objek Fisik | YOLO Class | Produk di App | Conf | Kondisi | ✓/✗ |
|---|-------------|-----------|---------------|------|---------|-----|
| 1 | Botol air | `bottle` | Aqua Mineral 600ml | 0.__ | Cahaya normal | |
| 2 | Buku | `book` | Buku Tulis Sinar Dunia | 0.__ | Cahaya normal | |
| 3 | Ponsel | `cell phone` | Samsung Galaxy A15 | 0.__ | Cahaya normal | |
| 4 | Botol air | `bottle` | | | Cahaya redup | |
| 5 | Buku | `book` | | | Tertutup sebagian | |
| 6 | Bebas | | | | Kondisi pilihan Anda | |

**Hitung:**
```
Success Rate = (jumlah ✓) ÷ (total percobaan) × 100%
```

**Pertanyaan:**
1. Kondisi apa yang menghasilkan confidence paling tinggi?
2. Kondisi apa yang paling sering gagal atau salah?
3. Jika confidence = 0.42, apakah Anda akan percaya hasilnya untuk transaksi nyata?

📸 **Checkpoint B:** Tabel terisi + angka success rate.

---

### 7.4 Tahap C — Transaksi Lengkap (70–90 menit)

1. Scan **2× botol air** → tekan `SPACE` dua kali
2. Pindah ke tab **📋 Katalog** → cari `book` → double-click → tambah 1
3. Tekan `C` (Checkout) → masukkan nominal bayar: misalnya `50000`
4. Lihat **kembalian otomatis** + rincian **pecahan uang**
5. Klik **✓ Proses Pembayaran**

**Cek output yang dihasilkan:**
```
output/
├── transactions.csv    ← buka dengan Excel atau Google Sheets
├── inspections.csv     ← log dari tombol [S]
└── receipts/
    └── INV-*.txt       ← struk teks
```

**Contoh baris `transactions.csv`:**
```
INV-20261027-103500, OPERATOR-01, MNM-001,
Aqua Botol Mineral 600ml, 2, 4500, 9000, 50000, 41000
```
*2 botol × Rp 4.500 = Rp 9.000 | Bayar Rp 50.000 | Kembalian Rp 41.000*

**Coba edit harga:**
Buka `data/catalog.json` → ubah `"price_idr": 4500` pada `bottle` menjadi `6000`
→ simpan → jalankan ulang → scan botol → harga di keranjang berubah menjadi Rp 6.000 ✅

📸 **Checkpoint C:** Screenshot dialog checkout + CSV terbuka di Excel.

---

### 7.5 Tahap D — Privacy Detective (90–100 menit)

Tentukan status setiap skenario: **Aman / Perlu Izin / Dilarang**

| # | Skenario | Status | Alasan Singkat |
|---|----------|--------|----------------|
| 1 | Scan botol Aqua, tidak ada orang di frame | | |
| 2 | Webcam menangkap wajah pelanggan di belakang produk | | |
| 3 | Scan struk belanja yang ada nomor telepon pemilik | | |
| 4 | Foto rak produk di toko tanpa ada orang | | |
| 5 | Rekam video aktivitas kasir seharian tanpa izin mereka | | |

**Cek langsung:** Buka folder `output/` — apakah ada foto wajah tersimpan saat tekan `S`?

---

### 7.6 Tahap E — Business Studio (100–120 menit)

**Buat diagram alur sistem:**
```
Kamera
  │
  ▼
[YOLO Detection]
  │
  ├──▶ person / chair / car ──▶ DIABAIKAN (blacklist 54 kelas)
  │
  └──▶ bottle / book / phone ──▶ Cocok di catalog.json
                                        │
                                Panel "Deteksi Sekarang"
                                (nama produk + harga + brand)
                                        │
                              Operator tekan [SPACE]
                                        │
                                  Keranjang Belanja
                                        │
                              Operator tekan [C]
                                        │
                        ┌──────────────┴──────────────┐
                        ▼                              ▼
                transactions.csv               Struk .txt
                        │
                        ▼
                Excel / Dashboard Manajer
```

**Isi tabel analisis:**

| Pertanyaan | Jawaban Anda |
|------------|-------------|
| Siapa saja aktor dalam sistem? | |
| 3 data wajib setiap transaksi | |
| 2 validasi sebelum data disimpan | |
| 1 KPI yang bisa diukur dari CSV | |
| 2 risiko utama sistem ini | |

---

### 7.7 Tahap F — Refleksi (120–130 menit)

Jawab **4 pertanyaan** ini, minimal 2–3 kalimat per jawaban:

**1. Kapan model gagal?**
Deskripsikan 1 kondisi nyata dari eksperimen Anda di mana AI salah atau tidak mendeteksi.

**2. Konsekuensi bisnis jika salah?**
`laptop` (Rp 5.499.000) terdeteksi sebagai `book` (Rp 7.500) dan langsung diproses — apa kerugiannya? Siapa yang dirugikan?

**3. Mengapa operator harus konfirmasi?**
Sistem meminta `SPACE` sebelum menambah item. Apakah lebih baik dibuat otomatis?
Berikan argumen pro dan kontra.

**4. Apa yang perlu ditambah untuk produksi nyata?**
Sebutkan **3 hal konkret** yang harus ada sebelum bisa dipakai di kasir toko sesungguhnya.

---

### 7.8 Retail AI Quest — Kumpulkan XP!

| Level | Tantangan | XP |
|-------|-----------|-----|
| 🟢 Starter | GUI aktif + bounding box terlihat | 10 |
| 🔵 Explorer | Deteksi 3 jenis produk berbeda | 15 |
| 🟡 Analyst | Tabel 6 eksperimen + success rate dihitung | 20 |
| 🟠 Developer | Edit catalog.json + transaksi + CSV valid | 25 |
| 🔴 Business Boss | Diagram sistem + KPI + 2 risiko | 20 |
| ⭐ Privacy Guardian | Privacy Detective 5 skenario dijawab | 10 |
| 🏆 BONUS | Tambah 1 produk baru ke catalog.json | +10 |

**Total: 100 XP = nilai penuh** *(+10 XP bonus)*

---

### 7.9 Yang Dikumpulkan ke Moodle

Buat ZIP bernama: **`NamaNIM_SmartRetail.zip`**

```
✅ screenshot_A_gui.png           GUI aktif + bounding box
✅ screenshot_C_checkout.png      Dialog checkout + kembalian
✅ screenshot_C_csv_excel.png     transactions.csv di Excel
✅ tabel_eksperimen.pdf           6+ baris + success rate
✅ diagram_sistem.png             Diagram dari Tahap E
✅ refleksi.pdf                   4 jawaban Tahap F
✅ privacy_detective.pdf          Tabel 5 skenario + alasan
✅ sawit/ (folder)                Output tugas sawit
```

> ⚠️ Hapus atau blur wajah dan data pribadi sebelum mengumpulkan!

---

## 8. Tugas Sawit

### Konteks Bisnis

Indonesia adalah produsen minyak sawit terbesar di dunia (±47 juta ton/tahun).
Kualitas CPO bergantung pada ketepatan grading **Tandan Buah Segar (TBS)** di loading ramp.

**Masalah saat ini:**
- Grading manual oleh petugas — subjektif dan tidak konsisten antar shift
- Tidak ada data digital → susah dianalisis manajemen
- Skala besar: ratusan ton TBS masuk per hari

### Kelas Kematangan TBS

| Kelas | Tampilan | Nilai Bisnis |
|-------|---------|-------------|
| 🟢 Unripe (Mentah) | Warna hitam/hijau, sedikit brondolan | Minyak rendah, harga rendah |
| 🟡 Ripe (Matang) | Warna jingga/merah, brondolan berjatuhan | Minyak optimal, harga terbaik |
| 🔴 Overripe (Lewat Matang) | Banyak brondolan jatuh, warna gelap | Asam lemak bebas tinggi, kualitas turun |

### Skema SawitVision

```
TBS di        ┌─────────┐   ┌─────────────────┐   ┌──────────────────┐
Loading  ────▶│ Kamera  │──▶│  YOLO Custom    │──▶│ Petugas Validasi │
Ramp          │ IP / HD │   │ (TBS Dataset!)  │   │  Human-in-Loop   │
              └─────────┘   └─────────────────┘   └────────┬─────────┘
                                                            │
                                                            ▼
                                                   ┌────────────────┐
                                                   │   Database     │──▶ Dashboard QC
                                                   └────────────────┘
```

---

### Langkah 1 — Lihat Dataset Publik TBS (20 menit)

Kita gunakan dataset **yang sudah tersedia** — tidak perlu kumpulkan foto sendiri.

**Akses Roboflow Universe:**
1. Buka **https://universe.roboflow.com**
2. Di kolom pencarian ketik: `oil palm bunch`
3. Pilih dataset yang muncul, contoh: *Oil Palm Fresh Fruit Bunch*
4. Klik tab **Images** → lihat contoh foto TBS yang sudah berlabel
5. Klik tab **Classes** → lihat kategori (Ripe, Unripe, Overripe)

**Yang dicatat di laporan:**
- Nama dataset yang dipilih
- Jumlah gambar total
- Kelas/kategori yang tersedia
- URL dataset

**Alternatif — Kaggle:**
1. Buka **https://www.kaggle.com/datasets**
2. Cari: `palm oil fresh fruit bunch`

---

### Langkah 2 — Eksperimen Scan Foto TBS (20 menit)

Download 3 foto dari dataset Roboflow (klik kanan gambar → **Save Image As**):
- 1 foto TBS **matang** (warna jingga/merah)
- 1 foto TBS **mentah** (warna hitam/hijau)
- 1 foto TBS yang **sulit dinilai**

Scan dengan aplikasi:

**🪟 Windows:**
```
python app.py --image foto_tbs_matang.jpg
```

**🍎 macOS:**
```bash
python3 app.py --image foto_tbs_matang.jpg
```

Catat hasilnya:

| # | Nama File | Terdeteksi Sebagai | Confidence | Ada di Catalog? |
|---|-----------|-------------------|-----------|----------------|
| 1 | foto_tbs_matang.jpg | | | Ya / Tidak |
| 2 | foto_tbs_mentah.jpg | | | Ya / Tidak |
| 3 | foto_tbs_sulit.jpg | | | Ya / Tidak |

**Pertanyaan (jawab di laporan):**
1. Apa yang dideteksi model dari foto TBS? Apakah relevan?
2. Mengapa model COCO tidak bisa mengenali TBS dengan tepat?
3. Apa artinya ini untuk perusahaan sawit yang mau pakai AI?

---

### Langkah 3 — Rancang Sistem SawitVision (40 menit)

Tidak perlu coding. Cukup **gambar dan jelaskan** sistem yang diusulkan.

**Tabel perbandingan — isi kolom kanan:**

| Aspek | Smart Retail Inspector (sudah jalan) | SawitVision (usulan Anda) |
|-------|--------------------------------------|--------------------------|
| Objek yang dideteksi | Botol, buku, ponsel (COCO) | |
| Model AI | Pretrained COCO, generik | |
| Data training | 80 kelas COCO, jutaan gambar | |
| Cara operator konfirmasi | Tekan `SPACE` di laptop | |
| Data yang disimpan | CSV: produk, qty, harga, struk | |
| Lingkungan operasi | Indoor, meja kasir, cahaya stabil | |
| Skala | 1 kasir, puluhan produk/hari | |

**Jawab pertanyaan bisnis (2–4 kalimat masing-masing):**

1. Mengapa tidak bisa langsung pakai model retail kita untuk sawit?
2. Data apa yang harus dikumpulkan sebelum sistem bisa dibangun? *(referensi: dataset Roboflow di Langkah 1)*
3. Siapa saja yang terlibat dalam sistem SawitVision?
4. Apa 2 manfaat utama untuk bisnis perusahaan sawit?
5. Apa 2 risiko jika sistem diterapkan tanpa persiapan matang?

---

### Langkah 4 — Refleksi (25 menit)

Jawab 3 pertanyaan berikut, masing-masing 3–5 kalimat:

**Refleksi 1 — Teknologi**
Dari percobaan di Langkah 2, model tidak mengenali TBS dengan tepat.
Apa yang harus dilakukan untuk membuat model yang bisa mengenali TBS?
Jelaskan dengan bahasa sederhana.

**Refleksi 2 — Bisnis**
Jika SawitVision berhasil dibangun dengan akurasi 90%, keputusan bisnis apa
yang bisa diambil manajer dari data yang terkumpul?
Berikan 2 contoh keputusan konkret.

**Refleksi 3 — Etika**
Kamera di loading ramp merekam pekerja setiap hari.
- Apa yang perlu disiapkan perusahaan agar pekerja menerima sistem ini?
- Siapa yang bertanggung jawab jika AI salah grade dan perusahaan rugi?

---

### Output Tugas Sawit

Buat folder `sawit/` di dalam ZIP pengumpulan:

```
sawit/
  laporan_sawitvision.pdf       ← Langkah 1–4 dalam format laporan
  screenshot_roboflow.png       ← Screenshot halaman dataset di Roboflow/Kaggle
  tabel_eksperimen_tbs.png      ← Screenshot tabel Langkah 2 yang sudah diisi
  screenshot_scan_tbs_1.png     ← Hasil scan foto TBS matang di aplikasi
  screenshot_scan_tbs_2.png     ← Hasil scan foto TBS mentah di aplikasi
  diagram_sawitvision.png       ← Gambar diagram sistem Langkah 3
```

> Gunakan `TEORI.md` di repo ini sebagai referensi untuk laporan.

---

## 9. Troubleshooting

### Error Saat Install

| Error | OS | Solusi |
|-------|-----|--------|
| `ModuleNotFoundError: cv2` | Semua | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | Semua | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | Semua | `pip install Pillow` |
| `Microsoft Visual C++ required` | Windows | Install Build Tools dari https://visualstudio.microsoft.com/visual-cpp-build-tools/ |
| `error: command 'gcc' failed` | macOS | `xcode-select --install` |
| `py not recognized` | Windows | Centang **Add to PATH** saat install Python, lalu restart terminal |

### Masalah Kamera

| Masalah | OS | Solusi |
|---------|-----|--------|
| Kamera hitam / tidak terbuka | Windows | Settings → Privacy → Camera → aktifkan akses |
| Kamera tidak terbuka | macOS | System Settings → Privacy → Camera → izinkan Terminal |
| Kamera tidak ditemukan | Semua | `python app.py --camera 1` (coba index lain: 0, 1, 2) |
| Gambar lag / FPS rendah | Semua | Normal di CPU tanpa GPU — tutup browser & aplikasi berat |

### Masalah Saat Jalankan

| Masalah | Solusi |
|---------|--------|
| Tombol keyboard tidak respons | Klik jendela GUI dulu (bukan terminal atau area tabel) |
| Objek tidak terdeteksi | Tambah cahaya · jarak 30–60cm · `--conf 0.25` |
| Download model gagal | Butuh internet ~50MB sekali, pastikan koneksi stabil |
| Tidak punya webcam | `python app.py --image foto_produk.jpg` |
| `(.venv)` tidak muncul | Jalankan ulang perintah aktivasi virtual environment |
| Port kamera dipakai app lain | Tutup Zoom, Teams, Google Meet, lalu coba lagi |

---

## Struktur Repo

```
ComputerVision/
├── app.py               ← Aplikasi utama (jalankan ini)
├── requirements.txt     ← 4 library Python yang dibutuhkan
├── README.md            ← Panduan lengkap ini
├── TEORI.md             ← Teori Computer Vision + referensi akademik
├── .gitignore
│
├── data/
│   ├── catalog.json     ← 20 produk nyata (boleh edit)
│   └── receipt_demo.png ← Demo gambar struk untuk OCR
│
├── output/              ← Hasil runtime (tidak di-push ke GitHub)
│   ├── transactions.csv
│   ├── inspections.csv
│   └── receipts/
│
└── tests/
    └── test_business.py ← 18 unit tests otomatis
```

---

## Lisensi

MIT License — bebas digunakan untuk keperluan pendidikan.
Model YOLO: [Ultralytics AGPL-3.0](https://github.com/ultralytics/ultralytics)

---

*AI untuk Bisnis — Sistem Informasi | © 2026 Triandes Sinaga*
