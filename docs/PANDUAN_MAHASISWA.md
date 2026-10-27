# 📖 Panduan Praktikum Mandiri
## Smart Retail Inspector — AI Computer Vision untuk Bisnis

> **Durasi:** 150 menit  
> **Level:** Pemula — tidak perlu pengalaman AI sebelumnya  
> **Yang dibutuhkan:** Laptop + webcam + botol/buku/ponsel/gunting

---

## 🎬 Cerita Proyek

Anda baru bergabung sebagai **Junior Business Analyst** di startup retail Indonesia.

Manajer Anda berkata:

> *"Kita mau coba AI untuk bantu kasir scan produk lebih cepat.  
> Tolong buat prototipe dulu — pakai laptop biasa.  
> Saya mau lihat apakah ini feasible sebelum kita investasi lebih jauh."*

Hari ini Anda akan **membuktikan konsepnya** (Proof of Concept):
- Apakah AI bisa mengenali produk dari kamera?
- Apakah datanya bisa otomatis tercatat ke sistem?
- Di mana batas kemampuannya?

---

## 🧠 Cara Kerja Sistem (Baca Dulu — 10 Menit)

### Pipeline dari Kamera ke Data

```
┌──────────┐     ┌─────────────────┐     ┌────────────────────────┐
│  Webcam  │────▶│   YOLO Model    │────▶│    catalog.json        │
│  Laptop  │     │  (AI Deteksi)   │     │  (Pemetaan Bisnis)     │
└──────────┘     └─────────────────┘     └────────────────────────┘
                        │                          │
                  "bottle"  0.87          "Aqua 600ml — Rp 4.500"
                        │                    Brand: Aqua
                        │
                 [SPACE] ← Anda konfirmasi
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
| **Confidence** | Skor keyakinan: `0.87` = AI 87% yakin |
| **COCO** | Dataset 80 kategori benda yang dipakai melatih model ini |
| **Blacklist** | Kelas yang diabaikan: `person`, `car`, `chair`, dll |

### ⚠️ Batasan Yang Wajib Dipahami

> Model YOLO ini mengenali **kategori generik**, bukan merek.
>
> `cell phone` bisa berarti Samsung, iPhone, atau Xiaomi — model tidak tahu bedanya.
> Inilah mengapa **operator harus konfirmasi** (tekan SPACE) sebelum data masuk.
>
> Sistem ini adalah **prototipe pendidikan**. Bukan kasir produksi.

---

## ⚙️ TAHAP A — Setup (0–20 Menit)

### A1. Clone / Download Proyek

```bash
git clone https://github.com/triandessinaga/ComputerVision.git
cd ComputerVision
```

Atau download ZIP dari GitHub → Extract → buka di VS Code.

### A2. Buat Virtual Environment

```bash
# Cek Python tersedia (butuh 3.10–3.12)
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

> Jika PowerShell menolak (execution policy), jalankan sekali:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

### A3. Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu ±3–7 menit. Library yang diinstall:
- `ultralytics` — YOLO object detection
- `opencv-python` — baca webcam & proses gambar
- `Pillow` — render frame ke GUI Tkinter

### A4. Verifikasi Instalasi

```bash
python -m unittest discover -s tests -v
```

Harus muncul:
```
Ran 18 tests in 0.001s
OK
```

### A5. Jalankan!

```bash
python app.py
```

Model YOLO (~50MB) diunduh otomatis pertama kali — butuh internet.
Setelah itu bisa dijalankan offline.

**📸 Checkpoint A:** Screenshot terminal menampilkan `OK` dan GUI terbuka.

---

## 📷 TAHAP B — Kenali Aplikasi (20–40 Menit)

### Layout GUI

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 Smart Retail Inspector            👤 OPERATOR-01   🕐 Waktu  │
├──────────────────────────┬───────────────────────────────────────┤
│  📷 AI Kamera  │📋 Katalog│        🛒 Keranjang Belanja           │
│                           │                                       │
│  ┌────────────┐  🎥Kontrol│  Produk      Qty   Harga   Subtotal  │
│  │            │  ──────── │  ─────────────────────────────────── │
│  │  KAMERA    │  ▶Aktifkan│                                       │
│  │  LIVE      │  ■ Stop   │                                       │
│  │            │  ──────── │  Total:                  Rp 0        │
│  └────────────┘  🎯Deteksi│  [💳 CHECKOUT [C]]                    │
│  ✅ Feedback area ⌨Shortcut│  [🔄 Reset [N]]                       │
└──────────────────────────┴───────────────────────────────────────┘
```

### Coba Langsung

1. Klik tab **📷 AI Kamera**
2. Di panel kanan kamera, klik **▶ Aktifkan Kamera**
3. Arahkan **botol air** ke webcam (jarak 30–60 cm, cahaya cukup)
4. Lihat panel **🎯 Deteksi Sekarang** — nama produk & confidence muncul
5. Tekan **`SPACE`** → produk masuk keranjang kanan
6. Tekan **`C`** → lihat dialog checkout dengan kembalian otomatis

**📸 Checkpoint B:** Screenshot GUI dengan bounding box aktif dan 1 produk di keranjang.

---

## 🧪 TAHAP C — Eksperimen (40–90 Menit)

### Worksheet Eksperimen

Lakukan **minimal 6 percobaan** dengan kondisi berbeda:

| # | Objek Fisik | YOLO Class | Produk di App | Conf | Kondisi | ✓/✗ |
|---|-------------|-----------|---------------|------|---------|------|
| 1 | Botol air | `bottle` | Aqua Mineral 600ml | | Cahaya normal | |
| 2 | Buku | `book` | Buku Tulis Sinar Dunia | | Cahaya normal | |
| 3 | Ponsel | `cell phone` | Samsung Galaxy A15 | | Cahaya normal | |
| 4 | Botol air | `bottle` | | | Cahaya redup | |
| 5 | Buku | `book` | | | Tertutup sebagian | |
| 6 | Bebas | | | | Kondisi pilihan Anda | |

### Hitung Success Rate

```
Success Rate = (jumlah ✓) ÷ (total percobaan) × 100%
```

### Pertanyaan Analisis

1. Kondisi apa yang membuat confidence **paling tinggi**?
2. Kondisi apa yang paling sering **salah** atau gagal?
3. Jika confidence = 0.42, apakah Anda percaya hasilnya untuk transaksi uang nyata? Jelaskan.

**📸 Checkpoint C:** Tabel terisi lengkap + angka success rate.

---

## 💳 TAHAP D — Transaksi Lengkap (90–110 Menit)

### Lakukan Transaksi

1. Scan **2× botol air** → tekan `SPACE` dua kali
2. Pindah tab **📋 Katalog** → double-click `book` → tambah 1
3. Tekan **`C`** (Checkout)
4. Masukkan uang bayar: misal `50000`
5. Lihat kembalian otomatis + rincian pecahan uang
6. Klik **✓ Proses Pembayaran**

### Cek Output yang Dihasilkan

Buka folder `output/` di VS Code atau Explorer:

```
output/
├── transactions.csv      ← Buka dengan Excel — ini data transaksi Anda
├── inspections.csv       ← Log inspeksi dari tombol [S]
└── receipts/
    └── INV-*.txt         ← Struk belanja dalam format teks
```

**Contoh baris di `transactions.csv`:**
```
INV-20261027-103500,2026-10-27T10:35:00,OPERATOR-01,MNM-001,
Aqua Botol Mineral 600ml,2,4500,9000,50000,41000
```

Bisa baca artinya?
- `2` botol × Rp `4.500` = `Rp 9.000`
- Dibayar `Rp 50.000` → kembalian `Rp 41.000`

### Edit Harga Produk

Buka `data/catalog.json`, ubah harga `bottle`:
```json
"bottle": {
    "sku": "MNM-001",
    "product": "Aqua Botol Mineral 600ml",
    "brand": "Aqua (Danone)",
    "price_idr": 6000
}
```
Simpan → jalankan ulang `python app.py` → scan botol lagi.
Harga di keranjang sekarang Rp 6.000? ✅ Itulah cara **business mapping** bekerja.

**📸 Checkpoint D:** Screenshot checkout dialog + CSV terbuka di Excel.

---

## 🔒 TAHAP E — Privacy Detective (110–120 Menit)

Tentukan status setiap skenario — **Aman / Perlu Izin / Dilarang**:

| # | Skenario | Status | Alasan Singkat |
|---|----------|--------|----------------|
| 1 | Scan botol Aqua, tidak ada orang di frame | | |
| 2 | Webcam menangkap wajah pelanggan di belakang produk | | |
| 3 | Scan struk yang ada nomor telepon pemilik | | |
| 4 | Foto rak produk di toko tanpa ada orang | | |
| 5 | Rekam video kerja kasir seharian tanpa izin mereka | | |

**Cek sendiri:** Buka folder `output/*.jpg` — apakah ada foto wajah Anda tersimpan saat tekan `S`?
Apakah data dikirim ke server internet? (Jawab: tidak — semua lokal)

---

## 🏗️ TAHAP F — Business Studio (120–140 Menit)

### Buat Diagram Sistem

Gambar alur ini di kertas, draw.io, atau PowerPoint:

```
Kamera Laptop
     │
     ▼
[YOLO Detection]
     │
     ├──▶ person/chair/car ──▶ DIABAIKAN (blacklist)
     │
     └──▶ bottle/book/phone ──▶ Cocok di catalog.json
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
                            ┌──────────┴───────────┐
                            ▼                       ▼
                    transactions.csv          Struk .txt
                            │
                            ▼
                    Excel / Dashboard
                    Laporan Manajer
```

### Isi Tabel Analisis

| Pertanyaan | Jawaban Anda |
|------------|-------------|
| Siapa aktor dalam sistem? | |
| 3 data wajib setiap transaksi | |
| 2 validasi sebelum data disimpan | |
| 1 KPI yang bisa diukur dari CSV | |
| 2 risiko utama | |

---

## 💬 TAHAP G — Refleksi (140–150 Menit)

Jawab **4 pertanyaan** ini secara tertulis (minimal 2–3 kalimat):

**1. Kapan model gagal?**
Deskripsikan 1 kondisi nyata dari eksperimen Anda di mana AI salah atau tidak mendeteksi.

**2. Konsekuensi bisnis jika salah?**
Jika `laptop` (Rp 5.499.000) terdeteksi sebagai `book` (Rp 7.500) dan langsung diproses — apa kerugiannya? Siapa yang dirugikan?

**3. Mengapa operator tetap harus konfirmasi?**
Sistem meminta SPACE sebelum menambah item ke keranjang. Apakah lebih baik dibuat otomatis? Berikan argumen pro dan kontra.

**4. Apa yang perlu ditambah untuk produksi nyata?**
Sebutkan **3 hal konkret** yang harus ada sebelum sistem ini bisa dipakai di kasir toko sungguhan.

---

## 🎮 Retail AI Quest — Kumpulkan XP!

| Level | Tantangan | XP |
|-------|-----------|-----|
| 🟢 **Starter** | GUI aktif + bounding box terlihat di kamera | 10 |
| 🔵 **Explorer** | Deteksi 3 jenis produk berbeda | 15 |
| 🟡 **Analyst** | Tabel 6 eksperimen + success rate dihitung | 20 |
| 🟠 **Developer** | Edit catalog.json + transaksi + CSV valid | 25 |
| 🔴 **Business Boss** | Diagram sistem + KPI + 2 risiko | 20 |
| ⭐ **Privacy Guardian** | Privacy Detective semua dijawab + alasan | 10 |
| 🏆 **BONUS** | Tambah 1 produk baru ke catalog.json | +10 |

**Total: 100 XP = nilai penuh** *(+10 XP bonus)*

---

## 🌴 Tugas Lanjutan: SawitVision

Lihat **[TUGAS_SAWIT.md](TUGAS_SAWIT.md)** untuk tugas mandiri transfer ke industri kelapa sawit.

---

## 📦 Yang Dikumpulkan ke Moodle

Buat ZIP: `NamaNIM_SmartRetail.zip`

```
✅ screenshot_A_gui_terbuka.png         GUI aktif
✅ screenshot_B_bbox_keranjang.png      Bounding box + produk di keranjang
✅ screenshot_D_checkout.png            Dialog checkout + kembalian
✅ screenshot_D_excel_csv.png           transactions.csv terbuka di Excel
✅ tabel_eksperimen.pdf                 6+ baris + success rate
✅ diagram_sistem.png                   Diagram alur dari Tahap F
✅ refleksi.pdf                         Jawaban 4 pertanyaan Tahap G
✅ privacy_detective.pdf                Tabel 5 skenario + alasan
✅ sawit/ (folder)                      Output Tugas Sawit (lihat TUGAS_SAWIT.md)
```

> ⚠️ **Pastikan:** Tidak ada wajah orang atau data pribadi di screenshot yang dikumpulkan!

---

## 🆘 Troubleshooting Cepat

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Kamera hitam / tidak buka | Tutup Zoom/Teams, cek Settings → Privacy → Camera |
| Kamera tidak ditemukan | `python app.py --camera 1` |
| Tombol tidak respons | Klik jendela utama GUI dulu (bukan terminal) |
| Objek tidak terdeteksi | Tambah cahaya · jarak 30–60cm · `--conf 0.25` |
| FPS lambat | Normal di CPU — tutup browser & aplikasi berat lain |
| Tidak punya webcam | `python app.py --image foto_produk.jpg` |

---

*Selamat mencoba! Kalau stuck, post pertanyaan di forum Moodle* 🚀
