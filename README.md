# 🔍 Smart Retail Inspector
### AI Computer Vision for Business — Praktikum Mandiri

[![Python](https://img.shields.io/badge/Python-3.10--3.12-blue?logo=python)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> **Mata Kuliah:** AI untuk Bisnis / Sistem Informasi  
> **Dosen:** Triandes Sinaga  
> **Durasi:** 150 menit praktikum + 120 menit tugas sawit  
> **Level:** Pemula — tidak perlu GPU, tidak perlu pengalaman AI

---

## 🎯 Apa yang Akan Dibangun?

Aplikasi desktop **real-time** yang menggunakan kamera laptop untuk:
- Mendeteksi produk dengan AI (YOLO)
- Mencocokkan ke produk nyata e-commerce Indonesia
- Mencatat ke keranjang belanja dengan konfirmasi operator
- Menghasilkan **struk `.txt`** + **data CSV** siap analisis Excel

```
Webcam → YOLO AI → Produk Terdeteksi → [SPACE] → Keranjang → [C] Checkout → CSV + Struk
```

---

# 🛠️ BAGIAN 1 — BANGUN DARI NOL

> Ini adalah jalur utama. Ikuti step by step dari awal.  
> Jika ada kendala teknis yang tidak bisa diselesaikan, lihat **Bagian 2 (Clone)** di bawah.

---

## LANGKAH 1 — Install Python

### Cek apakah Python sudah ada

Buka **Command Prompt** atau **PowerShell**, ketik:
```bash
py --version
```

Kalau muncul `Python 3.10.x` atau lebih baru → **lanjut ke Langkah 2**.

Kalau muncul error atau versi lama → install dulu:

1. Buka browser → pergi ke **https://python.org/downloads**
2. Klik tombol kuning besar **"Download Python 3.12.x"**
3. Jalankan installer yang diunduh
4. ⚠️ **WAJIB centang** kotak **"Add Python to PATH"** di bagian bawah installer
5. Klik **Install Now**
6. Setelah selesai, tutup dan buka ulang PowerShell
7. Verifikasi: `py --version` → harus muncul versi Python

---

## LANGKAH 2 — Siapkan Folder Proyek

Buat folder kosong untuk proyek. Contoh:
```
D:\Praktikum\SmartRetail\
```

Caranya:
1. Buka **File Explorer**
2. Masuk ke Drive D (atau lokasi yang Anda inginkan)
3. Klik kanan → **New Folder** → beri nama `SmartRetail`

Lalu buka folder itu di **VS Code**:
1. Buka VS Code
2. `File` → `Open Folder` → pilih folder `SmartRetail`
3. Buka terminal di VS Code: menu `Terminal` → `New Terminal`

---

## LANGKAH 3 — Buat Virtual Environment

Virtual environment adalah "ruang terisolasi" untuk Python — agar library yang diinstall tidak bercampur dengan proyek lain.

```bash
py -3 -m venv .venv
```

Setelah berhasil, akan muncul folder `.venv` di proyek Anda.

**Aktifkan virtual environment:**

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Jika muncul error **"execution policy"**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Ketik `Y` lalu Enter, kemudian coba aktifkan lagi.

```bash
# Windows CMD (alternatif)
.venv\Scripts\activate.bat
```

```bash
# macOS / Linux
source .venv/bin/activate
```

✅ Berhasil jika di terminal muncul `(.venv)` di awal baris.

---

## LANGKAH 4 — Buat File `requirements.txt`

Di VS Code, buat file baru bernama `requirements.txt` di root folder proyek.
Isi dengan:

```
ultralytics>=8.3,<9
opencv-python>=4.8,<5
Pillow>=10,<13
pytesseract>=0.3.10,<1
```

Simpan file (`Ctrl+S`).

---

## LANGKAH 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

Proses ini mengunduh dan menginstall:
- `ultralytics` — YOLO object detection AI
- `opencv-python` — baca webcam dan proses gambar
- `Pillow` — render frame ke GUI Tkinter
- `pytesseract` — OCR (opsional)

Tunggu **3–7 menit** hingga selesai. Output normal:
```
Successfully installed ultralytics-X.X opencv-python-X.X Pillow-X.X ...
```

---

## LANGKAH 6 — Buat File `data/catalog.json`

Buat folder `data/` di dalam proyek, lalu buat file `catalog.json`:

```json
{
  "_comment": "Mapping YOLO class ke produk nyata Indonesia",

  "bottle":     {"sku":"MNM-001","product":"Aqua Botol Mineral 600ml",         "brand":"Aqua",      "price_idr":4500,   "category":"Minuman"},
  "cup":        {"sku":"MNM-002","product":"Mie Sedaap Cup Ayam 75g",           "brand":"Wings Food","price_idr":5500,   "category":"Makanan Instan"},
  "book":       {"sku":"ATK-001","product":"Buku Tulis Sinar Dunia 58 Lembar",  "brand":"Sinar Dunia","price_idr":7500,  "category":"Alat Tulis"},
  "cell phone": {"sku":"ELK-001","product":"Samsung Galaxy A15",                "brand":"Samsung",   "price_idr":1899000,"category":"Smartphone"},
  "laptop":     {"sku":"ELK-002","product":"ASUS VivoBook 14 Intel i3",         "brand":"ASUS",      "price_idr":5499000,"category":"Laptop"},
  "keyboard":   {"sku":"ELK-003","product":"Keyboard Logitech K120 USB",        "brand":"Logitech",  "price_idr":175000, "category":"Aksesoris"},
  "mouse":      {"sku":"ELK-004","product":"Mouse Wireless Logitech M170",      "brand":"Logitech",  "price_idr":149000, "category":"Aksesoris"},
  "scissors":   {"sku":"ATK-002","product":"Gunting Joyko SC-809",              "brand":"Joyko",     "price_idr":18500,  "category":"Alat Tulis"},
  "banana":     {"sku":"BSY-001","product":"Pisang Ambon Lokal (per 100g)",     "brand":"Lokal",     "price_idr":3000,   "category":"Buah & Sayur"},
  "apple":      {"sku":"BSY-002","product":"Apel Fuji Import (per 100g)",       "brand":"Import",    "price_idr":4500,   "category":"Buah & Sayur"},
  "orange":     {"sku":"BSY-003","product":"Jeruk Medan Manis (per 100g)",      "brand":"Lokal",     "price_idr":3500,   "category":"Buah & Sayur"},
  "carrot":     {"sku":"BSY-004","product":"Wortel Segar (per 100g)",           "brand":"Lokal",     "price_idr":2000,   "category":"Buah & Sayur"},
  "remote":     {"sku":"ELK-005","product":"Remote TV Universal RM-L1268",      "brand":"Universal", "price_idr":35000,  "category":"Elektronik"},
  "clock":      {"sku":"ELK-006","product":"Jam Dinding Deli 12 Inch",          "brand":"Deli",      "price_idr":89000,  "category":"Elektronik"},
  "bowl":       {"sku":"RMH-001","product":"Mangkok Melamin Lion Star 15cm",    "brand":"Lion Star", "price_idr":12000,  "category":"Dapur"},
  "sandwich":   {"sku":"MKN-001","product":"Roti Tawar Sari Roti Jumbo 650g",   "brand":"Sari Roti", "price_idr":22500,  "category":"Makanan"},
  "pizza":      {"sku":"MKN-002","product":"Frozen Pizza Belfoods Royal 135g",  "brand":"Belfoods",  "price_idr":35000,  "category":"Makanan Beku"},
  "cake":       {"sku":"MKN-003","product":"Bolu Gulung Nabati Richeese",       "brand":"Nabati",    "price_idr":18000,  "category":"Snack"},
  "vase":       {"sku":"RMH-002","product":"Vas Bunga Keramik Dekorasi",        "brand":"Ikea",      "price_idr":79000,  "category":"Dekorasi"},
  "fork":       {"sku":"RMH-003","product":"Garpu Makan Stainless Steel 6 pcs", "brand":"Zebra",     "price_idr":32000,  "category":"Dapur"}
}
```

---

## LANGKAH 7 — Buat File `app.py`

Buat file `app.py` di root folder. Ini adalah aplikasi utama.

> 📌 **Salin kode dari repo GitHub:**
> Buka https://github.com/triandessinaga/ComputerVision/blob/main/app.py
> Klik tombol **Raw** → Select All → Copy → Paste ke file `app.py` Anda → Simpan

Atau unduh langsung:
```bash
curl -o app.py https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/app.py
```

---

## LANGKAH 8 — Buat File `tests/test_business.py`

Buat folder `tests/` lalu buat file `test_business.py`:

> 📌 Salin dari: https://github.com/triandessinaga/ComputerVision/blob/main/tests/test_business.py

Atau unduh:
```bash
mkdir tests
curl -o tests/test_business.py https://raw.githubusercontent.com/triandessinaga/ComputerVision/main/tests/test_business.py
```

---

## LANGKAH 9 — Buat Folder Output

```bash
mkdir output
```

Atau buat manual lewat File Explorer — buat folder bernama `output` di dalam proyek.

---

## LANGKAH 10 — Verifikasi

Jalankan unit tests untuk memastikan semua berjalan:

```bash
python -m unittest discover -s tests -v
```

Harus muncul:
```
test_all_have_required_fields ... ok
test_all_prices_positive ... ok
...
Ran 18 tests in 0.001s
OK
```

---

## LANGKAH 11 — Jalankan Aplikasi! 🚀

```bash
python app.py
```

Saat pertama kali, YOLO mengunduh model AI (~50MB) secara otomatis.
Tunggu hingga jendela GUI terbuka.

**Struktur folder Anda sekarang:**
```
SmartRetail/
├── .venv/
├── app.py
├── requirements.txt
├── data/
│   └── catalog.json
├── output/
└── tests/
    └── test_business.py
```

---

# 📖 BAGIAN 2 — PANDUAN PRAKTIKUM

## 🧠 Konsep Dasar (10 menit)

### Cara Kerja Sistem

```
┌──────────┐    ┌─────────────────┐    ┌────────────────────────┐
│  Webcam  │───▶│   YOLO Model    │───▶│    catalog.json        │
│  Laptop  │    │  (AI Deteksi)   │    │  (Pemetaan Bisnis)     │
└──────────┘    └─────────────────┘    └────────────────────────┘
                       │                          │
                 "bottle" 0.87          "Aqua 600ml — Rp 4.500"
                       │
                [SPACE] ← Anda konfirmasi dulu
                       │
             ┌─────────▼──────────┐
             │     Keranjang      │──▶ [C] Checkout ──▶ CSV + Struk
             └────────────────────┘
```

### Kosakata Penting

| Istilah | Artinya |
|---------|---------|
| **Frame** | 1 foto dari video (30 foto/detik = 30 FPS) |
| **Bounding Box** | Kotak yang mengelilingi objek terdeteksi |
| **YOLO Class** | Kategori objek: `bottle`, `book`, `cell phone`, dll |
| **Confidence** | Skor keyakinan AI: `0.87` = 87% yakin |
| **Blacklist** | Kelas diabaikan: `person`, `car`, `chair`, dll |

### ⚠️ Batasan Penting

> Model mengenali **kategori generik**, bukan merek.
> `cell phone` bisa Samsung, iPhone, atau Xiaomi — AI tidak tahu bedanya.
> Itulah mengapa operator **wajib konfirmasi** (`SPACE`) sebelum data masuk.

---

## ⌨️ Keyboard Shortcuts

| Tombol | Aksi |
|--------|------|
| `SPACE` | ✅ Tambah produk terdeteksi ke keranjang |
| `TAB` | 🔄 Ganti pilihan deteksi (jika > 1 objek) |
| `U` | ↩ Undo item terakhir |
| `C` | 💳 Checkout + kalkulator kembalian |
| `N` | 🔄 Reset keranjang |
| `S` | 💾 Simpan inspeksi ke CSV |
| `Q` / `Esc` | 🚪 Keluar |

---

## 🔧 Mode Jalankan

```bash
python app.py                    # webcam default
python app.py --camera 1         # webcam ke-2
python app.py --image foto.jpg   # gambar statis (tanpa webcam)
python app.py --conf 0.30        # lebih sensitif mendeteksi
```

---

## TAHAP A — Kenali Aplikasi (0–20 menit)

### Layout GUI

```
┌────────────────────────────────────────────────────────────────┐
│  🔍 Smart Retail Inspector         👤 OPERATOR-01   🕐 Waktu   │
├──────────────────────────┬─────────────────────────────────────┤
│  📷 AI Kamera  │📋 Katalog│       🛒 Keranjang Belanja          │
│  ┌────────────┐  🎥Kontrol│                                    │
│  │            │  ▶Aktifkan│  Produk   Qty   Harga   Subtotal  │
│  │  KAMERA    │  ■ Stop   │  ─────────────────────────────── │
│  │  LIVE 16:9 │           │                                    │
│  │            │  🎯Deteksi│  Total:              Rp 0          │
│  └────────────┘  ⌨Shortcut│  [💳 CHECKOUT  [C]]               │
│  ✅ Feedback     TERLIHAT  │  [🔄 Reset     [N]]               │
└──────────────────────────┴─────────────────────────────────────┘
```

### Coba Pertama

1. Klik tab **📷 AI Kamera**
2. Klik **▶ Aktifkan Kamera** di panel kanan
3. Arahkan botol air ke webcam (jarak 30–60 cm, cahaya cukup)
4. Panel **🎯 Deteksi Sekarang** menampilkan nama produk + confidence
5. Tekan `SPACE` → produk masuk keranjang
6. Tekan `C` → lihat dialog checkout dengan kembalian

**📸 Checkpoint A:** Screenshot GUI dengan bounding box aktif dan 1 produk di keranjang.

---

## TAHAP B — Eksperimen (20–70 menit)

### Tabel Eksperimen (isi minimal 6 baris)

| # | Objek Fisik | YOLO Class | Produk di App | Conf | Kondisi | ✓/✗ |
|---|-------------|-----------|---------------|------|---------|------|
| 1 | Botol air | `bottle` | Aqua Mineral 600ml | 0.__ | Cahaya normal | |
| 2 | Buku | `book` | Buku Tulis Sinar Dunia | 0.__ | Cahaya normal | |
| 3 | Ponsel | `cell phone` | Samsung Galaxy A15 | 0.__ | Cahaya normal | |
| 4 | Botol air | `bottle` | | | Cahaya redup | |
| 5 | Buku | `book` | | | Tertutup sebagian | |
| 6 | Bebas | | | | Kondisi pilihan Anda | |

### Hitung Success Rate

```
Success Rate = (jumlah ✓) ÷ (total percobaan) × 100%
```

**Pertanyaan:**
1. Kondisi apa yang membuat confidence paling tinggi?
2. Kondisi apa yang paling sering gagal?
3. Jika confidence = 0.42, percayakah Anda untuk transaksi uang nyata?

**📸 Checkpoint B:** Tabel terisi + angka success rate.

---

## TAHAP C — Transaksi Lengkap (70–90 menit)

1. Scan **2× botol** → `SPACE` dua kali
2. Tab **📋 Katalog** → double-click `book` → tambah 1
3. Tekan `C` → masukkan bayar: `50000`
4. Lihat kembalian + rincian pecahan uang otomatis
5. Klik **✓ Proses Pembayaran**

### Cek Output di Folder `output/`

```
output/transactions.csv      ← Buka di Excel
output/inspections.csv       ← Log dari [S]
output/receipts/INV-*.txt    ← Struk teks
```

**Contoh baris `transactions.csv`:**
```
INV-20261027-103500, OPERATOR-01, MNM-001,
Aqua Botol Mineral 600ml, 2, 4500, 9000, 50000, 41000
```
*2 × Rp 4.500 = Rp 9.000 | Bayar Rp 50.000 | Kembalian Rp 41.000*

### Edit Harga Produk

Buka `data/catalog.json`, ubah `price_idr` pada `bottle` dari `4500` → `6000`.
Simpan → jalankan ulang → scan botol → harga jadi Rp 6.000. ✅

**📸 Checkpoint C:** Screenshot checkout + CSV di Excel.

---

## TAHAP D — Privacy Detective (90–100 menit)

| # | Skenario | Status | Alasan |
|---|----------|--------|--------|
| 1 | Scan botol Aqua, tidak ada orang di frame | | |
| 2 | Webcam menangkap wajah pelanggan | | |
| 3 | Scan struk yang ada nomor telepon | | |
| 4 | Foto rak produk tanpa orang | | |
| 5 | Rekam video kasir seharian tanpa izin | | |

---

## TAHAP E — Business Studio (100–120 menit)

### Buat Diagram Alur

```
Kamera → [YOLO] → person/chair → DIABAIKAN
                → bottle/book  → Catalog Match
                                      │
                               Operator [SPACE]
                                      │
                               Keranjang [C]
                                      │
                         ┌────────────┴──────────┐
                         ▼                        ▼
                 transactions.csv           Struk .txt
                         │
                         ▼
                  Excel / Dashboard
```

| Pertanyaan | Jawaban |
|------------|---------|
| Aktor dalam sistem | |
| 3 data wajib per transaksi | |
| 2 validasi sebelum simpan | |
| 1 KPI dari CSV | |
| 2 risiko utama | |

---

## TAHAP F — Refleksi (120–130 menit)

1. **Kapan model gagal?** — 1 kondisi nyata dari eksperimen Anda
2. **Konsekuensi bisnis?** — `laptop` (Rp 5.499.000) terdeteksi sebagai `book` (Rp 7.500)?
3. **Mengapa operator konfirmasi?** — Pro dan kontra jika dibuat otomatis
4. **Siap produksi?** — 3 hal yang harus ditambah

---

## 🎮 Retail AI Quest — Kumpulkan XP!

| Level | Tantangan | XP |
|-------|-----------|-----|
| 🟢 **Starter** | GUI aktif + bounding box terlihat | 10 |
| 🔵 **Explorer** | Deteksi 3 jenis produk berbeda | 15 |
| 🟡 **Analyst** | Tabel 6 eksperimen + success rate | 20 |
| 🟠 **Developer** | Edit catalog + transaksi + CSV valid | 25 |
| 🔴 **Business Boss** | Diagram sistem + KPI + 2 risiko | 20 |
| ⭐ **Privacy Guardian** | Privacy Detective semua dijawab | 10 |
| 🏆 **BONUS** | Tambah 1 produk baru ke catalog.json | +10 |

**Total: 100 XP = nilai penuh**

---

## 📦 Yang Dikumpulkan ke Moodle

Buat ZIP: **`NamaNIM_SmartRetail.zip`**

```
✅ screenshot_A_gui.png              GUI aktif + bounding box
✅ screenshot_C_checkout.png         Dialog checkout + kembalian
✅ screenshot_C_csv_excel.png        CSV di Excel
✅ tabel_eksperimen.pdf              6+ baris + success rate
✅ diagram_sistem.png                Dari Tahap E
✅ refleksi.pdf                      4 jawaban Tahap F
✅ privacy_detective.pdf             Tabel 5 skenario
✅ sawit/ (folder)                   Tugas SawitVision (lihat bagian bawah)
```

---

## 🆘 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Kamera hitam / tidak buka | Tutup Zoom/Teams · Settings → Privacy → Camera |
| Kamera tidak ditemukan | `python app.py --camera 1` |
| Tombol keyboard tidak respons | Klik jendela GUI dulu, bukan terminal |
| Objek tidak terdeteksi | Tambah cahaya · jarak 30–60 cm · `--conf 0.25` |
| FPS lambat | Normal di CPU · tutup app berat lain |
| Download model gagal | Butuh internet ~50MB sekali saja |
| Tidak punya webcam | `python app.py --image foto_produk.jpg` |

---

# 🌴 BAGIAN 3 — TUGAS SAWIT

> **Durasi:** 120 menit di luar jam kelas  
> **Bobot:** 30% dari total nilai

---

## Konteks Bisnis

> Perusahaan sawit di Sumatera ingin menggunakan AI untuk menggantikan
> inspeksi manual kualitas **Tandan Buah Segar (TBS)** di loading ramp.
> Grading saat ini dilakukan petugas — lambat, subjektif, tidak konsisten antar shift.

---

## Skema Sistem SawitVision

```
TBS di       ┌─────────┐   ┌────────────────┐   ┌─────────────────┐
Loading ────▶│ Kamera  │──▶│  YOLO Custom   │──▶│ Petugas Validasi│
Ramp         │ IP / HD │   │ (TBS Dataset!) │   │  Human-in-Loop  │
             └─────────┘   └────────────────┘   └────────┬────────┘
                                                          │
                                                          ▼
                                                  ┌───────────────┐
                                                  │   Database    │──▶ Dashboard QC
                                                  └───────────────┘
```

---

## Bagian 1 — Analisis Gap (20 menit)

| Aspek | Smart Retail Inspector | SawitVision (jawaban Anda) |
|-------|----------------------|---------------------------|
| Objek | Botol, buku, ponsel | TBS — COCO tidak mengenali |
| Model YOLO | Pretrained generik | ❓ |
| Konfirmasi | Tekan `SPACE` | ❓ |
| Output | CSV + struk | ❓ |
| Lingkungan | Indoor, meja | ❓ Outdoor, loading ramp |
| Skala | Puluhan item/hari | ❓ Ratusan ton/hari |

---

## Bagian 2 — Eksperimen (30 menit)

Cari **3 foto TBS** dari sumber legal (tanpa wajah pekerja):

```bash
python app.py --image foto_tbs_matang.jpg
```

| Foto | Objek Nyata | Terdeteksi | Conf | Relevan? |
|------|-------------|-----------|------|----------|
| TBS Matang | Tandan buah | ??? | 0.__ | Ya/Tidak |
| TBS Mentah | Tandan buah | ??? | 0.__ | Ya/Tidak |
| TBS Sulit | Tandan buah | ??? | 0.__ | Ya/Tidak |

> **❓ Pertanyaan Kritis:** Model tidak mengenali TBS — apakah ini kegagalan AI
> atau justru pelajaran penting tentang batas model generik?
> Jelaskan implikasinya untuk bisnis sawit dalam 3–5 kalimat.

---

## Bagian 3 — Proposal Sistem (50 menit)

Buat proposal **1–2 halaman** berisi:

**3.1 Problem Statement**
- Apa kerugian bisnis jika grading TBS salah?

**3.2 Proposed Solution**
- Spesifikasi kamera di loading ramp
- Pretrained COCO atau model custom TBS?
- Cara operator konfirmasi

**3.3 Data Requirements**
```
□ _____ foto TBS per kelas (matang/mentah/over-ripe)
□ Label bounding box oleh: ____________________
□ Variasi: pagi/siang/sore, cerah/hujan, besar/kecil
□ Metadata per foto: __________________________
```

**3.4 Pilot KPI**

| KPI | Cara Mengukur |
|-----|---------------|
| Akurasi deteksi | Dibandingkan keputusan petugas ahli |
| Waktu per inspeksi | Dibandingkan waktu manual baseline |
| Tingkat override petugas | % keputusan AI yang dikoreksi |

> ⚠️ Jangan mengarang angka target. Tulis: *"Target ditetapkan setelah baseline manual diukur 2 minggu."*

**3.5 Risiko & Mitigasi**

| Risiko | Mitigasi |
|--------|---------|
| Model salah grade TBS matang → rugi per ton | |
| Kamera kotor di loading ramp | |
| Petugas senior menolak sistem AI | |
| Foto rekam identitas pekerja | |

**3.6 Roadmap**
```
Minggu 1–2:  Kumpulkan 200+ foto TBS per kelas, beri label
Minggu 3–4:  Fine-tuning YOLO dengan dataset TBS
Minggu 5:    Testing offline
Minggu 6–7:  Pilot di 1 loading ramp
Minggu 8:    Evaluasi → keputusan scale-up
```

---

## Bagian 4 — Refleksi Etika (20 menit)

**4.1** Kamera di loading ramp merekam pekerja setiap hari.
Apa yang harus dilakukan perusahaan **sebelum** memasang kamera?

**4.2** Jika AI salah grade dan perusahaan rugi besar —
siapa yang bertanggung jawab: pengembang, operator, atau manajer?

**4.3** Petugas senior 10 tahun menolak sistem AI karena merasa tidak dipercaya.
Bagaimana Anda mengelola perubahan ini?

---

## Output Tugas Sawit

Masukkan ke folder `sawit/` dalam ZIP:
```
sawit/
  proposal_sawitvision.pdf       Bagian 1–3
  tabel_eksperimen_tbs.pdf       Bagian 2 + analisis kritis
  refleksi_etika.pdf             Bagian 4
  foto_tbs_1.jpg + _2.jpg + _3.jpg
  screenshot_scan_tbs.png
```

---

# 🔽 BAGIAN 4 — ALTERNATIF: CLONE DARI GITHUB

> Gunakan ini jika mengalami kesulitan teknis dalam membangun dari nol,
> atau jika ingin langsung mencoba aplikasi yang sudah lengkap.

---

## Clone Proyek

```bash
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision
```

Jika belum punya Git, download installer dari **https://git-scm.com/download/win**
dan install dengan pengaturan default.

## Setup Setelah Clone

```bash
# Buat virtual environment
py -3 -m venv .venv

# Aktifkan
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Verifikasi
python -m unittest discover -s tests -v

# Jalankan!
python app.py
```

## Perbedaan Clone vs Bangun Sendiri

| Aspek | Bangun dari Nol | Clone |
|-------|-----------------|-------|
| Pemahaman kode | ✅ Lebih dalam | ⚡ Langsung jalan |
| Waktu setup | ~30 menit | ~10 menit |
| Cocok untuk | Belajar mandiri | Demo cepat |
| Nilai praktikum | ✅ Penuh | ✅ Penuh (dengan bukti) |

> 💡 Meskipun clone, Anda tetap harus melakukan semua eksperimen dan tugas sawit.
> Bedanya hanya di tahap setup awal.

---

## ⚠️ Disclaimer

Model YOLO pretrained COCO mengenali **kategori generik**, bukan merek/SKU spesifik.
Harga di `catalog.json` adalah **simulasi pendidikan**.
Untuk kasir produksi: butuh model custom, barcode scanner, dan validasi sistem penuh.

---

## 📝 Lisensi

MIT License — bebas digunakan untuk pendidikan.  
Model YOLO: [Ultralytics AGPL-3.0](https://github.com/ultralytics/ultralytics)

---

*AI untuk Bisnis — Sistem Informasi | © 2026 Triandes Sinaga*
