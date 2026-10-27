# 📖 Panduan Praktikum Mandiri
## Smart Retail Inspector — AI Computer Vision untuk Bisnis

> **Waktu:** 150 menit  
> **Prasyarat:** Python terinstall, laptop + webcam  
> **Yang dibawa:** Botol air minum, buku, gunting, atau ponsel

---

## 🎯 Cerita & Konteks

Anda baru bergabung sebagai **Junior Business Analyst** di startup retail.

Manajer Anda berkata:

> *"Tim kita mau coba pakai AI untuk bantu kasir scan produk.  
> Tolong buatkan prototipe dulu — pakai laptop biasa.  
> Presentasikan minggu depan apakah ini feasible."*

Tugas Anda hari ini: **Proof of Concept (PoC)** — buktikan bahwa AI bisa mengenali produk dari kamera dan datanya bisa dicatat secara otomatis.

---

## 🧠 Konsep Wajib Dipahami (15 menit)

### Pipeline Sistem

```
┌──────────┐   ┌────────────────┐   ┌──────────────────────┐
│  Webcam  │──▶│  YOLO Model    │──▶│   catalog.json       │
│ (input)  │   │ (AI detection) │   │ (business mapping)   │
└──────────┘   └────────────────┘   └──────────────────────┘
                      │                        │
               "bottle" 0.87          "Aqua 600ml - Rp 4.500"
                      │
               [SPACE] ← operator konfirmasi
                      │
              ┌───────▼────────┐
              │  Keranjang     │──▶ Checkout ──▶ CSV + Struk
              └────────────────┘
```

### Kosakata Teknis

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **Frame** | 1 foto dari video (30 foto/detik = 30 FPS) |
| **Bounding Box** | Kotak yang mengelilingi objek di gambar |
| **YOLO Class** | Kategori objek: `bottle`, `book`, `person`, dll |
| **Confidence** | Skor keyakinan AI: 0.87 artinya 87% yakin |
| **COCO Dataset** | 80 kategori benda yang dipakai melatih model ini |
| **Blacklist** | Kelas yang diabaikan: `person`, `car`, `chair`, dll |

### ⚠️ Yang Harus Anda Tahu

> Model ini mengenali **kategori generik**, bukan merek spesifik.
> `cell phone` bisa Samsung, iPhone, atau Xiaomi — model tidak tahu.
>
> Itulah mengapa operator **harus konfirmasi** sebelum data disimpan.
> Sistem ini dirancang untuk **demo dan pembelajaran**, bukan kasir produksi.

---

## 🔧 TAHAP A — Setup (0–20 menit)

### A1. Buka Project

1. Buka **VS Code**
2. `File` → `Open Folder` → pilih folder `ComputerVision`
3. Buka terminal: `Terminal` → `New Terminal`

### A2. Buat Virtual Environment

```bash
# Cek Python tersedia
py --version

# Buat environment terisolasi
py -3 -m venv .venv
```

Aktifkan:
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

> **Jika PowerShell ditolak:**
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> Lalu coba lagi.

### A3. Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu ±2–5 menit. Output normal:
```
Successfully installed ultralytics-X.X opencv-python-X.X Pillow-X.X ...
```

### A4. Verifikasi

```bash
python -m unittest discover -s tests -v
```

Harus muncul: `Ran 18 tests in 0.001s --- OK`

### A5. Jalankan Aplikasi!

```bash
python app.py
```

Model YOLO (~50MB) diunduh otomatis pertama kali. Tunggu jendela GUI terbuka.

**✅ Checkpoint A:** Screenshot terminal menampilkan `OK` dan GUI terbuka.

---

## 📷 TAHAP B — Kenali Aplikasi (20–40 menit)

### Layout GUI

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Smart Retail Inspector      👤 OPERATOR    🕐 Waktu      │
├──────────────────────────┬──────────────────────────────────┤
│  📷 AI Kamera │ 📋 Katalog│  🛒 Keranjang Belanja           │
│  ┌────────────┐  🎥Kontrol│                                  │
│  │            │  ▶Aktifkan│  Produk   Qty   Harga  Subtotal │
│  │  KAMERA    │  ■ Stop   │  ──────────────────────────────  │
│  │  LIVE      │           │                                  │
│  │            │  🎯Deteksi│                                  │
│  └────────────┘  ⌨Shortcut│  Total:              Rp 0       │
│  Feedback area  (TERLIHAT)│  [💳 CHECKOUT [C]]               │
│                           │  [🔄 Reset [N]]                  │
└──────────────────────────┴──────────────────────────────────┘
```

### Coba Langkah Pertama

1. Klik tab **📷 AI Kamera**
2. Di panel kanan kamera, klik tombol **▶ Aktifkan Kamera**
3. Arahkan **botol air** ke webcam (jarak 30–60 cm)
4. Lihat panel **🎯 Deteksi Sekarang** — nama produk dan confidence muncul
5. Tekan **`SPACE`** → produk masuk keranjang
6. Lihat keranjang di panel kanan bertambah

**✅ Checkpoint B:** Screenshot GUI dengan bounding box dan produk di keranjang.

---

## 🧪 TAHAP C — Eksperimen Terstruktur (40–90 menit)

### Worksheet Eksperimen

Lakukan minimal **6 percobaan** berbeda. Isi tabel ini:

| # | Objek Fisik | YOLO Class | Produk Terdeteksi | Conf | Kondisi | Benar? |
|---|-------------|-----------|-------------------|------|---------|--------|
| 1 | Botol air | bottle | Aqua Mineral 600ml | 0.__ | Cahaya normal | ✓/✗ |
| 2 | Buku | book | Buku Tulis Sinar Dunia | 0.__ | Cahaya normal | ✓/✗ |
| 3 | Ponsel | cell phone | Samsung Galaxy A15 | 0.__ | Cahaya normal | ✓/✗ |
| 4 | Botol air | bottle | | | Redup/malam | ✓/✗ |
| 5 | Buku | book | | | Tertutup sebagian | ✓/✗ |
| 6 | Objek bebas | | | | Kondisi Anda pilih | ✓/✗ |

### Analisis

Setelah tabel terisi, hitung:

```
Success Rate = (jumlah ✓ / total percobaan) × 100%
```

Jawab pertanyaan ini:
1. Pada kondisi apa confidence paling tinggi?
2. Pada kondisi apa model paling sering salah?
3. Jika confidence = 0.45, apakah Anda akan percaya hasilnya untuk transaksi nyata?

**✅ Checkpoint C:** Tabel 6+ baris + success rate terhitung.

---

## 💳 TAHAP D — Simulasi Transaksi (90–110 menit)

### Lakukan Transaksi Lengkap

1. Scan 2 botol air (`SPACE` × 2)
2. Scan 1 buku (`SPACE` × 1)
3. Tekan **`C`** → dialog checkout terbuka
4. Masukkan nominal bayar (misal: 50000)
5. Lihat **kembalian otomatis** + rincian pecahan uang
6. Klik **✓ Proses Pembayaran**
7. Struk muncul di dialog

### Cek Data Output

```
output/
  transactions.csv     ← buka dengan Excel
  inspections.csv      ← buka dengan Excel
  receipts/INV-*.txt   ← buka dengan Notepad
```

### Edit Katalog

Buka `data/catalog.json`, ubah harga `bottle`:
```json
"bottle": {
    "sku": "MNM-001",
    "product": "Aqua Botol Mineral 600ml",
    "price_idr": 6000
}
```
Simpan → jalankan ulang `python app.py` → scan botol lagi.

Harga di keranjang berubah? **Itulah cara mapping bisnis bekerja.**

**✅ Checkpoint D:** Screenshot checkout + CSV terbuka di Excel.

---

## 🔒 TAHAP E — Privacy Detective (110–120 menit)

Tentukan status setiap skenario: **Aman / Perlu Izin / Dilarang**

| # | Skenario | Status | Alasan |
|---|----------|--------|--------|
| 1 | Scan botol Aqua, tidak ada orang di frame | | |
| 2 | Webcam menangkap wajah pelanggan di belakang produk | | |
| 3 | Scan struk belanja yang memuat nomor telepon | | |
| 4 | Foto rak produk di toko tanpa orang | | |
| 5 | Rekam video kerja kasir seharian tanpa izin | | |

Pertanyaan tambahan:
- Cek folder `output/` — apakah ada foto wajah tersimpan?
- Apakah sistem ini mengirim data ke server?

---

## 🏗️ TAHAP F — Business Studio (120–140 menit)

### Buat Diagram Alur Sistem

Gambar di kertas atau digital (draw.io, Figma, PowerPoint):

```
Kamera
  │
  ▼
[YOLO Detection]
  │
  ├── person → DIABAIKAN (blacklist)
  ├── chair  → DIABAIKAN (blacklist)
  │
  └── bottle → CATALOG MATCH
                  │
                  ▼
            Operator lihat hasil
                  │
            [SPACE] konfirmasi
                  │
                  ▼
            Keranjang bertambah
                  │
                  ▼
              [C] Checkout
                  │
            ┌─────┴─────┐
            ▼           ▼
        CSV Log      Struk .txt
            │
            ▼
      Dashboard Manajer
```

### Isi tabel ini:

| Elemen | Jawaban Anda |
|--------|-------------|
| Aktor dalam sistem | |
| 3 data wajib di setiap transaksi | |
| 2 validasi sebelum data disimpan | |
| 1 KPI yang bisa diukur | |
| 2 risiko utama | |

---

## 💬 TAHAP G — Refleksi (140–150 menit)

Jawab 4 pertanyaan ini (minimal 2 kalimat per jawaban):

**1. Kapan model gagal?**
Deskripsikan 1 kondisi nyata di mana AI salah mendeteksi.

**2. Apa konsekuensi bisnis jika salah?**
Jika `laptop` (Rp 5.499.000) terdeteksi sebagai `book` (Rp 7.500) — apa yang terjadi pada transaksi?

**3. Mengapa operator tetap harus konfirmasi?**
Sistem ini meminta SPACE sebelum menambah item — apakah ini tepat? Jelaskan.

**4. Apakah siap untuk toko nyata?**
Sebutkan minimal 3 hal yang harus ditambahkan sebelum bisa digunakan di produksi.

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

**Total: 100 XP untuk nilai penuh** (+ 10 XP bonus)

---

## 📦 File yang Dikumpulkan

Buat ZIP bernama: `NamaNIM_SmartRetail.zip`

```
✅ screenshot_webcam_aktif.png         GUI + bounding box
✅ screenshot_checkout.png             Dialog checkout + kembalian
✅ output/transactions.csv             Min. 1 transaksi
✅ output/inspections.csv              Min. 3 inspeksi [S]
✅ output/receipts/INV-*.txt           Struk transaksi
✅ tabel_eksperimen.pdf                6+ baris + success rate
✅ diagram_sistem.png                  Alur sistem
✅ refleksi.pdf                        4 jawaban refleksi
✅ privacy_detective.pdf               Jawaban 5 skenario
```

> **Hapus wajah dan data pribadi** sebelum mengumpulkan!

---

## 🌴 Tugas Lanjutan

Lihat file **[TUGAS_SAWIT.md](TUGAS_SAWIT.md)** untuk tugas transfer ke industri kelapa sawit.

---

## 🆘 Troubleshooting Cepat

```bash
# Error: No module named 'cv2'
pip install opencv-python

# Error: No module named 'ultralytics'
pip install ultralytics

# Error: No module named 'PIL'
pip install Pillow

# Kamera tidak terbuka
python app.py --camera 1

# Objek tidak terdeteksi
python app.py --conf 0.25

# Tidak punya webcam
python app.py --image foto_produk.jpg
```

---

*Good luck! Jika ada pertanyaan, post di forum Moodle* 🚀
