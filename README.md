# 🔍 Smart Retail Inspector
### AI Computer Vision for Business — Praktikum Mandiri

[![Python](https://img.shields.io/badge/Python-3.10--3.12-blue?logo=python)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> **Mata Kuliah:** AI untuk Bisnis / Sistem Informasi  
> **Dosen:** Triandes Sinaga  
> **Durasi:** 150 menit praktikum + 120 menit tugas sawit  
> **Level:** Pemula — tidak perlu GPU, tidak perlu pengalaman AI sebelumnya

---

## 🎬 Apa yang Akan Anda Bangun?

Aplikasi desktop **real-time** yang menggunakan kamera laptop untuk:
- Mendeteksi produk dengan AI (YOLO)
- Mencocokkan ke 20 produk nyata e-commerce Indonesia
- Mencatat ke keranjang belanja dengan konfirmasi operator
- Menghasilkan **struk `.txt`** + **data CSV** siap analisis Excel

```
Webcam → YOLO AI → Produk Terdeteksi → [SPACE] → Keranjang → [C] Checkout → Struk + CSV
```

---

## ⚡ MULAI CEPAT — 5 Menit

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

> Model YOLO (~50MB) diunduh **otomatis** saat pertama kali dijalankan. Butuh internet sekali.

**Tidak punya webcam?**
```bash
python app.py --image foto_produk.jpg
```

---

## ⌨️ Keyboard Shortcuts

| Tombol | Aksi |
|--------|------|
| `SPACE` | ✅ Tambah produk terdeteksi ke keranjang |
| `TAB` | 🔄 Ganti pilihan deteksi (jika > 1 objek) |
| `U` | ↩ Undo item terakhir |
| `C` | 💳 Checkout + kalkulator kembalian otomatis |
| `N` | 🔄 New — reset keranjang |
| `S` | 💾 Simpan inspeksi ke CSV (tanpa checkout) |
| `Q` / `Esc` | 🚪 Keluar |

---

## 📁 Struktur Proyek

```
ComputerVision/
│
├── app.py               ← 🎯 File utama, jalankan ini
├── requirements.txt     ← 4 library: ultralytics, opencv, pillow, pytesseract
├── README.md            ← Panduan lengkap ini
│
├── data/
│   ├── catalog.json     ← 📦 20 produk real (edit harga di sini)
│   └── receipt_demo.png ← Demo OCR struk
│
├── output/              ← 📊 Hasil otomatis saat program jalan
│   ├── transactions.csv ← Log transaksi [C]
│   ├── inspections.csv  ← Log inspeksi [S]
│   └── receipts/        ← Struk .txt per transaksi
│
└── tests/
    └── test_business.py ← 18 unit tests
```

---

## 📦 Katalog — 20 Produk Real Indonesia

Setiap kelas YOLO dipetakan ke produk nyata yang dijual di Tokopedia/Shopee/Alfamart:

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
| `sandwich` | Roti Tawar Sari Roti Jumbo 650g | Sari Roti | Rp 22.500 |
| `remote` | Remote TV Universal RM-L1268 | Universal | Rp 35.000 |
| `clock` | Jam Dinding Deli 12 Inch | Deli | Rp 89.000 |
| `bowl` | Mangkok Melamin Polos 15cm | Lion Star | Rp 12.000 |
| `fork` | Garpu Makan Stainless Steel (6 pcs) | Zebra | Rp 32.000 |
| `pizza` | Frozen Pizza Belfoods Royal 135g | Belfoods | Rp 35.000 |
| `cake` | Bolu Gulung Nabati Richeese | Nabati | Rp 18.000 |
| `vase` | Vas Bunga Keramik Dekorasi | Ikea | Rp 79.000 |

> **Kelas yang diabaikan (blacklist):** `person`, `car`, `chair`, `cat`, `dog`, dan 49 kelas lain — tidak akan masuk keranjang meskipun terdeteksi.

> **Edit harga:** Buka `data/catalog.json`, ubah nilai `price_idr`, simpan, jalankan ulang.

---

## 🔧 Mode Jalankan

```bash
python app.py                    # webcam default
python app.py --camera 1         # webcam ke-2 / eksternal
python app.py --image foto.jpg   # gambar statis (tanpa webcam)
python app.py --conf 0.30        # turunkan threshold agar lebih sensitif
```

---

## 🧪 Unit Tests

```bash
python -m unittest discover -s tests -v
# Ran 18 tests in 0.001s — OK
```

---

## 📊 Output yang Dihasilkan

### `output/transactions.csv` — dibuat saat `[C]` Checkout
```
invoice,timestamp,kasir,sku,product,qty,unit_price,line_total,payment,change
INV-20261027-103500,2026-10-27T10:35:00,OPERATOR-01,MNM-001,
Aqua Botol Mineral 600ml,2,4500,9000,50000,41000
```
*2 botol × Rp 4.500 = Rp 9.000 | Bayar Rp 50.000 | Kembalian Rp 41.000*

### `output/inspections.csv` — dibuat saat `[S]`
```
timestamp,sample_id,source,yolo_class,sku,product,category,price_idr,confidence,operator_confirmed
2026-10-27T10:30:00,ITEM-001,WEBCAM,bottle,MNM-001,Aqua Botol Mineral 600ml,Minuman,4500,0.876,YES
```

---

# 📖 PANDUAN PRAKTIKUM — Step by Step

## 🧠 Konsep Wajib Dipahami (10 menit)

### Pipeline Sistem

```
┌──────────┐    ┌─────────────────┐    ┌───────────────────────┐
│  Webcam  │───▶│   YOLO Model    │───▶│    catalog.json       │
│  Laptop  │    │  (AI Deteksi)   │    │  (Pemetaan Bisnis)    │
└──────────┘    └─────────────────┘    └───────────────────────┘
                       │                         │
                 "bottle" 0.87         "Aqua 600ml — Rp 4.500"
                       │                    Brand: Aqua
                       │
                [SPACE] ← Anda konfirmasi dulu
                       │
             ┌─────────▼──────────┐
             │     Keranjang      │──▶ [C] Checkout ──▶ CSV + Struk
             └────────────────────┘
```

### Kosakata Teknis

| Istilah | Artinya |
|---------|---------|
| **Frame** | 1 foto dari video (30 foto/detik = 30 FPS) |
| **Bounding Box** | Kotak yang mengelilingi objek yang dideteksi |
| **YOLO Class** | Kategori objek: `bottle`, `book`, `cell phone`, dll |
| **Confidence** | Skor keyakinan AI: `0.87` = 87% yakin |
| **COCO** | Dataset 80 kategori benda untuk melatih model YOLO ini |
| **Blacklist** | Kelas yang diabaikan sistem: `person`, `car`, `chair`, dll |

### ⚠️ Batasan Penting

> Model mengenali **kategori generik**, bukan merek spesifik.
> `cell phone` bisa Samsung, iPhone, atau Xiaomi — AI tidak tahu bedanya.
>
> Itulah mengapa operator **wajib konfirmasi** (tekan `SPACE`) sebelum data masuk.
> Ini adalah **prototipe pendidikan**, bukan sistem kasir produksi.

---

## ⚙️ TAHAP A — Setup (0–20 Menit)

Ikuti langkah di bagian **Mulai Cepat** di atas.

Setelah berhasil, verifikasi:
```bash
python -m unittest discover -s tests -v
# Harus: Ran 18 tests ... OK
```

**📸 Checkpoint A:** Screenshot terminal menampilkan `OK` dan jendela GUI terbuka.

---

## 📷 TAHAP B — Kenali Aplikasi (20–40 Menit)

### Layout GUI

```
┌────────────────────────────────────────────────────────────────┐
│  🔍 Smart Retail Inspector         👤 OPERATOR-01   🕐 Waktu   │
├──────────────────────────┬─────────────────────────────────────┤
│  📷 AI Kamera  │📋 Katalog│       🛒 Keranjang Belanja          │
│  ┌────────────┐  🎥Kontrol│  Produk     Qty    Harga  Subtotal │
│  │            │  ▶Aktifkan│  ──────────────────────────────── │
│  │  KAMERA    │  ■ Stop   │                                    │
│  │  LIVE 16:9 │           │                                    │
│  │            │  🎯Deteksi│  Total:              Rp 0          │
│  └────────────┘  ⌨Shortcut│  [💳 CHECKOUT  [C]]               │
│  ✅ Feedback     TERLIHAT  │  [🔄 Reset     [N]]               │
└──────────────────────────┴─────────────────────────────────────┘
```

### Coba Langkah Pertama

1. Klik tab **📷 AI Kamera**
2. Di panel kanan kamera, klik **▶ Aktifkan Kamera**
3. Arahkan **botol air** ke webcam — jarak 30–60 cm, cahaya cukup
4. Lihat panel **🎯 Deteksi Sekarang** — nama produk + confidence muncul
5. Tekan **`SPACE`** → produk masuk keranjang kanan
6. Tekan **`C`** → lihat dialog checkout dengan kembalian otomatis

**📸 Checkpoint B:** Screenshot GUI dengan bounding box aktif dan 1 produk di keranjang.

---

## 🧪 TAHAP C — Eksperimen (40–90 Menit)

### Tabel Eksperimen (isi minimal 6 baris)

| # | Objek Fisik | YOLO Class | Produk di App | Conf | Kondisi | ✓/✗ |
|---|-------------|-----------|---------------|------|---------|------|
| 1 | Botol air | `bottle` | Aqua Mineral 600ml | 0.__ | Cahaya normal | |
| 2 | Buku | `book` | Buku Tulis Sinar Dunia | 0.__ | Cahaya normal | |
| 3 | Ponsel | `cell phone` | Samsung Galaxy A15 | 0.__ | Cahaya normal | |
| 4 | Botol air | `bottle` | | | Cahaya redup/malam | |
| 5 | Buku | `book` | | | Tertutup sebagian | |
| 6 | Bebas | | | | Kondisi pilihan Anda | |

### Hitung Success Rate

```
Success Rate = (jumlah ✓) ÷ (total percobaan) × 100%
```

### Pertanyaan Analisis

1. Kondisi apa yang membuat confidence **paling tinggi**?
2. Kondisi apa yang paling sering **gagal**?
3. Jika confidence = 0.42, apakah Anda percaya hasilnya untuk transaksi uang nyata?

**📸 Checkpoint C:** Tabel terisi lengkap + angka success rate.

---

## 💳 TAHAP D — Transaksi Lengkap (90–110 Menit)

### Lakukan Ini Step by Step

1. Scan **2× botol air** → tekan `SPACE` dua kali
2. Pindah tab **📋 Katalog** → double-click produk `book` → tambah 1
3. Tekan **`C`** (Checkout)
4. Masukkan bayar: `50000`
5. Lihat kembalian + rincian **pecahan uang** otomatis
6. Klik **✓ Proses Pembayaran**

### Cek Output

Buka folder `output/` di VS Code atau File Explorer:

```
output/transactions.csv      ← Buka dengan Excel
output/inspections.csv       ← Log inspeksi dari [S]
output/receipts/INV-*.txt    ← Struk teks
```

**Contoh baris `transactions.csv` yang akan Anda lihat:**
```
INV-20261027-103500, 2026-10-27T10:35:00, OPERATOR-01,
MNM-001, Aqua Botol Mineral 600ml, 2, 4500, 9000, 50000, 41000
```
Bisa baca? → 2 × Rp 4.500 = Rp 9.000 | Bayar Rp 50.000 | Kembalian Rp 41.000

### Edit Harga — Coba Sendiri

Buka `data/catalog.json`, ubah harga `bottle` dari `4500` → `6000`:
```json
"bottle": {
    "sku": "MNM-001",
    "product": "Aqua Botol Mineral 600ml",
    "price_idr": 6000
}
```
Simpan → `python app.py` → scan botol → harga di keranjang jadi Rp 6.000.  
**Itulah cara business mapping bekerja.**

**📸 Checkpoint D:** Screenshot dialog checkout + CSV terbuka di Excel.

---

## 🔒 TAHAP E — Privacy Detective (110–120 Menit)

Tentukan **Aman / Perlu Izin / Dilarang** untuk setiap skenario:

| # | Skenario | Status | Alasan |
|---|----------|--------|--------|
| 1 | Scan botol Aqua, tidak ada orang di frame | | |
| 2 | Webcam menangkap wajah pelanggan di belakang produk | | |
| 3 | Scan struk belanja yang ada nomor telepon | | |
| 4 | Foto rak produk di toko tanpa ada orang | | |
| 5 | Rekam video kerja kasir seharian tanpa izin mereka | | |

**Cek langsung:** Buka `output/*.jpg` — adakah foto wajah Anda tersimpan saat tekan `S`?

---

## 🏗️ TAHAP F — Business Studio (120–140 Menit)

### Buat Diagram Alur Sistem

```
Kamera Laptop
      │
      ▼
[YOLO Detection]
      │
      ├──▶ person / chair / car ──▶ DIABAIKAN (blacklist)
      │
      └──▶ bottle / book / phone ──▶ Cocok di catalog.json
                                            │
                                            ▼
                                   Panel "Deteksi Sekarang"
                                   (nama produk + harga + brand)
                                            │
                                   Operator tekan [SPACE]
                                            │
                                            ▼
                                     Keranjang Belanja
                                            │
                                   Operator tekan [C]
                                            │
                               ┌────────────┴────────────┐
                               ▼                          ▼
                       transactions.csv            Struk .txt
                               │
                               ▼
                       Excel / Dashboard
                       Laporan Manajer
```

### Isi Tabel Analisis Sistem

| Pertanyaan | Jawaban Anda |
|------------|-------------|
| Siapa saja aktor dalam sistem? | |
| 3 data wajib per transaksi | |
| 2 validasi sebelum data disimpan | |
| 1 KPI yang bisa diukur dari CSV | |
| 2 risiko utama sistem ini | |

---

## 💬 TAHAP G — Refleksi (140–150 Menit)

Jawab **4 pertanyaan** berikut (minimal 2–3 kalimat per jawaban):

**1. Kapan model gagal?**
Deskripsikan 1 kondisi dari eksperimen Anda di mana AI salah atau tidak mendeteksi.

**2. Konsekuensi bisnis jika salah?**
Jika `laptop` (Rp 5.499.000) terdeteksi sebagai `book` (Rp 7.500) dan langsung diproses — apa kerugiannya?

**3. Mengapa operator tetap harus konfirmasi?**
Sistem meminta `SPACE` sebelum menambah item. Lebih baik dibuat otomatis? Argumen pro dan kontra.

**4. Apa yang perlu ditambah untuk produksi nyata?**
Sebutkan **3 hal konkret** yang harus ada sebelum dipakai di kasir toko sesungguhnya.

---

## 🎮 Retail AI Quest — Kumpulkan XP!

| Level | Tantangan | XP |
|-------|-----------|-----|
| 🟢 **Starter** | GUI aktif + bounding box terlihat | 10 |
| 🔵 **Explorer** | Deteksi 3 jenis produk berbeda | 15 |
| 🟡 **Analyst** | Tabel 6 eksperimen + success rate | 20 |
| 🟠 **Developer** | Edit catalog.json + transaksi + CSV valid | 25 |
| 🔴 **Business Boss** | Diagram sistem + KPI + 2 risiko | 20 |
| ⭐ **Privacy Guardian** | Privacy Detective semua dijawab | 10 |
| 🏆 **BONUS** | Tambah 1 produk baru ke catalog.json | +10 |

**Total: 100 XP = nilai penuh** *(+10 XP bonus)*

---

## 📦 Yang Dikumpulkan ke Moodle

Buat ZIP: **`NamaNIM_SmartRetail.zip`**

```
✅ screenshot_A_gui.png              GUI aktif + terminal OK
✅ screenshot_B_bbox.png             Bounding box + produk di keranjang
✅ screenshot_D_checkout.png         Dialog checkout + kembalian
✅ screenshot_D_csv_excel.png        transactions.csv di Excel
✅ tabel_eksperimen.pdf              6+ baris + success rate
✅ diagram_sistem.png                Diagram alur dari Tahap F
✅ refleksi.pdf                      4 jawaban Tahap G
✅ privacy_detective.pdf             Tabel 5 skenario
✅ sawit/ (folder)                   Tugas SawitVision (lihat bagian bawah)
```

> ⚠️ Pastikan tidak ada wajah atau data pribadi di file yang dikumpulkan!

---

# 🌴 TUGAS SAWIT — Transfer ke Industri

> **Durasi:** 120 menit (di luar jam kelas)  
> **Bobot:** 30% dari total nilai praktikum

---

## 🎯 Konteks Bisnis

Anda sudah membangun Smart Retail Inspector yang mendeteksi produk di kasir.

Sekarang **transfer konsep yang sama** ke industri kelapa sawit:

> Perusahaan sawit di Sumatera ingin menggunakan AI untuk menggantikan
> inspeksi manual kualitas **Tandan Buah Segar (TBS)** di loading ramp.
> Grading saat ini dilakukan petugas — lambat, subjektif, tidak konsisten antar shift.

---

## 📐 Skema Sistem SawitVision

```
                ┌──────────────────────────────────────────┐
                │          SAWITVISION SYSTEM               │
                │                                           │
TBS di       ┌──┴──┐   ┌────────────┐   ┌───────────────┐  │
Loading ────▶│Kamera│──▶│ YOLO Model │──▶│ Business Rules│  │
Ramp         │ IP  │   │ (Custom!)  │   │    Engine     │  │
             └──┬──┘   └────────────┘   └───────┬───────┘  │
                │                               │           │
                │               ┌───────────────┘           │
                │               ▼                           │
                │     ┌──────────────────┐                  │
                │     │ Petugas Validasi  │                  │
                │     │  (Human-in-Loop) │                  │
                │     └────────┬─────────┘                  │
                │              │ Konfirmasi                  │
                │              ▼                            │
                │     ┌──────────────────┐                  │
                │     │    Database       │──▶ Dashboard QC  │
                │     │  (Inspeksi Log)  │    Manajer        │
                │     └──────────────────┘                  │
                └──────────────────────────────────────────┘
```

---

## 📋 Bagian 1 — Analisis Gap (20 menit)

Bandingkan sistem retail dengan kebutuhan sawit:

| Aspek | Smart Retail Inspector | SawitVision (isi jawaban Anda) |
|-------|----------------------|-------------------------------|
| Objek yang dideteksi | Botol, buku, ponsel (COCO) | TBS — model COCO tidak mengenali ini |
| Model YOLO | Pretrained generik | ❓ Pretrained atau custom? |
| Cara konfirmasi | Tekan `SPACE` | ❓ |
| Output data | CSV transaksi + struk | ❓ |
| Lingkungan | Indoor, meja kasir | ❓ Outdoor, loading ramp |
| Skala operasi | Puluhan item/hari | ❓ Ratusan ton/hari |
| Keahlian operator | Kasir umum | ❓ |

---

## 🧪 Bagian 2 — Eksperimen Langsung (30 menit)

**Langkah 1:** Cari 3 foto TBS dari internet (sumber legal, tanpa wajah pekerja):
- 1 foto TBS **matang** (warna jingga/merah)
- 1 foto TBS **mentah** (warna hijau/hitam)
- 1 foto TBS **sulit dinilai** (campuran)

**Langkah 2:** Scan foto di aplikasi:
```bash
python app.py --image foto_tbs_matang.jpg
```

**Langkah 3:** Catat hasilnya:

| Foto | Objek Nyata | Terdeteksi sebagai | Conf | Relevan? |
|------|-------------|-------------------|------|----------|
| TBS Matang | Tandan buah sawit | ??? | 0.__ | Ya / Tidak |
| TBS Mentah | Tandan buah sawit | ??? | 0.__ | Ya / Tidak |
| TBS Sulit | Tandan buah sawit | ??? | 0.__ | Ya / Tidak |

**❓ Pertanyaan Kritis:**
> Model TIDAK mengenali TBS. Apakah ini berarti AI-nya gagal?
> Atau justru ini pelajaran penting tentang keterbatasan model generik?
> Jelaskan dalam 3–5 kalimat — dan apa implikasinya untuk bisnis sawit.

---

## 📝 Bagian 3 — Proposal Sistem (50 menit)

Buat proposal **1–2 halaman** dengan struktur ini:

### 3.1 Problem Statement
- Apa yang terjadi jika grading TBS salah satu grade?
- Berapa estimasi kerugian per ton jika salah grade?
- Mengapa solusi manual tidak cukup untuk skala industri?

### 3.2 Proposed Solution
Gambar ulang skema SawitVision di atas dengan detail spesifik:
- Spesifikasi kamera: IP camera? Resolusi berapa? Posisi pemasangan?
- Jenis model: pretrained COCO (seperti sekarang) atau perlu custom training?
- Bagaimana petugas melakukan konfirmasi?
- Di mana data disimpan — local database atau cloud?

### 3.3 Data Requirements
```
Untuk pilot minimal yang credible:
  □ _____ foto TBS per kelas kematangan (matang/mentah/over-ripe)
  □ Label/anotasi bounding box oleh: ____________________
  □ Variasi kondisi yang harus dicakup:
      □ Pagi / siang / sore
      □ Cerah / mendung / hujan
      □ TBS besar / kecil
  □ Metadata wajib per foto: _____________________________
```

### 3.4 Pilot KPI (3 metrik terukur)

| KPI | Cara Mengukur | Catatan |
|-----|---------------|---------|
| Akurasi deteksi per kelas | | Target ditetapkan setelah baseline manual diukur |
| Waktu inspeksi per truk | | Bandingkan dengan waktu manual |
| Tingkat override petugas | | Berapa % keputusan AI dikoreksi petugas |

> ⚠️ Jangan mengarang angka target. Tuliskan: *"Target ditetapkan setelah mengukur baseline manual selama 2 minggu."*

### 3.5 Risiko & Mitigasi

| Risiko | Dampak Bisnis | Mitigasi |
|--------|--------------|---------|
| Model salah grade TBS matang → dihitung mentah | Rugi per ton | |
| Kamera kotor / rusak di loading ramp | Sistem mati | |
| Petugas tidak percaya sistem AI | Resistensi adopsi | |
| Foto berisi identitas pekerja | Pelanggaran privasi | |

### 3.6 Roadmap 8 Minggu

```
Minggu 1–2:  Pengumpulan foto TBS berlabel (min. 200/kelas, 3 kelas)
Minggu 3–4:  Fine-tuning YOLO dengan dataset TBS
Minggu 5:    Testing offline di laboratorium
Minggu 6–7:  Pilot di 1 loading ramp dengan pengawasan ketat
Minggu 8:    Evaluasi data → keputusan scale-up atau revisi
```

**Pertanyaan:** Apa risikonya jika langsung ke Minggu 6 tanpa Minggu 1–5?

---

## 🔒 Bagian 4 — Refleksi Etika (20 menit)

**4.1 Hak Pekerja**
Kamera di loading ramp merekam aktivitas pekerja setiap hari.
Apa yang harus dilakukan perusahaan *sebelum* memasang kamera?
(Petunjuk: pikirkan tentang persetujuan, informasi, dan tujuan penggunaan)

**4.2 Akuntabilitas Keputusan**
Jika AI salah grade dan perusahaan rugi 50 juta rupiah dalam sebulan —
siapa yang bertanggung jawab: pengembang AI, operator yang konfirmasi,
atau manajer yang memutuskan pakai sistem?

**4.3 Kepercayaan & Perubahan**
Petugas senior 10 tahun grading TBS merasa tidak dipercaya karena digantikan AI.
Bagaimana Anda sebagai analyst sistem mengelola resistensi ini?

---

## 📦 Output Tugas Sawit

Buat folder `sawit/` di dalam ZIP pengumpulan:

```
sawit/
  proposal_sawitvision.pdf         Bagian 1–3 format laporan
  tabel_eksperimen_tbs.pdf         Tabel Bagian 2 + analisis kritis
  refleksi_etika.pdf               Jawaban Bagian 4
  foto_tbs_1.jpg                   Foto yang digunakan (tanpa wajah)
  foto_tbs_2.jpg
  foto_tbs_3.jpg
  screenshot_scan_tbs.png          Hasil scan foto TBS di aplikasi
```

---

## 🆘 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Kamera hitam / tidak terbuka | Tutup Zoom/Teams · Settings → Privacy → Camera |
| Kamera tidak ditemukan | `python app.py --camera 1` |
| Tombol keyboard tidak respons | Klik area jendela GUI dulu, bukan terminal |
| Objek tidak terdeteksi | Tambah cahaya · jarak 30–60 cm · `--conf 0.25` |
| FPS lambat | Normal di CPU — tutup browser & app berat lain |
| Download model gagal | Butuh internet ~50MB sekali saat pertama |
| Tidak punya webcam | `python app.py --image foto_produk.jpg` |

---

## ⚠️ Disclaimer

Model YOLO pretrained COCO mengenali **kategori generik**, bukan merek/SKU spesifik.
Harga di `catalog.json` adalah **simulasi pendidikan**. Untuk kasir produksi nyata
dibutuhkan: model custom, barcode scanner, integrasi ERP, dan validasi keamanan penuh.

---

## 📝 Lisensi

MIT License — bebas digunakan untuk pendidikan.  
Model YOLO: [Ultralytics AGPL-3.0](https://github.com/ultralytics/ultralytics)

---

*AI untuk Bisnis — Sistem Informasi | © 2026 Triandes Sinaga*
