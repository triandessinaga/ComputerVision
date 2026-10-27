# 🌴 Tugas Transfer: SawitVision
## Dari Retail Inspector ke Inspeksi Tandan Buah Segar (TBS)

> **Tugas Mandiri Lanjutan:** 120 menit (di luar jam kelas)  
> **Dikumpulkan bersama:** NamaNIM_SmartRetail.zip  
> **Bobot:** 30% dari total nilai praktikum

---

## 🎯 Latar Belakang

Anda sudah membangun **Smart Retail Inspector** yang mendeteksi produk dengan AI.

Sekarang bayangkan skenario berbeda:

> Sebuah perusahaan kelapa sawit di Sumatera ingin mengadopsi Computer Vision
> untuk **inspeksi kualitas Tandan Buah Segar (TBS)** di loading ramp.
> Saat ini, grading TBS dilakukan secara manual oleh petugas — lambat, subjektif,
> dan tidak konsisten antar shift.
>
> CEO meminta tim IT untuk mengkaji apakah AI bisa membantu.

**Tugas Anda:** Buat **proposal teknis** berdasarkan apa yang sudah Anda pelajari hari ini.

---

## 📐 Skema Sistem yang Diusulkan

```
                    ┌─────────────────────────────────────────┐
                    │         SAWIT VISION SYSTEM              │
                    │                                          │
  TBS di         ┌──┴──┐    ┌──────────┐    ┌──────────────┐  │
  Loading  ────▶ │Kamera│──▶ │YOLO Model│──▶ │ Business     │  │
  Ramp           │ IP  │    │ (Custom) │    │ Rules Engine │  │
                 └──┬──┘    └──────────┘    └──────┬───────┘  │
                    │                              │           │
                    │              ┌───────────────┘           │
                    │              ▼                            │
                    │    ┌──────────────────┐                  │
                    │    │ Petugas Validasi  │                  │
                    │    │ (Human-in-Loop)  │                  │
                    │    └────────┬─────────┘                  │
                    │             │ Konfirmasi                  │
                    │             ▼                            │
                    │    ┌──────────────────┐                  │
                    │    │    Database       │──▶ Dashboard     │
                    │    │  (Inspeksi Log)  │    Manajer QC    │
                    │    └──────────────────┘                  │
                    └─────────────────────────────────────────┘
```

---

## 📋 Instruksi Tugas

### Bagian 1 — Analisis Gap (20 menit)

Bandingkan **Retail Inspector** dengan kebutuhan **SawitVision**:

| Aspek | Smart Retail Inspector | SawitVision (yang dibutuhkan) |
|-------|----------------------|-------------------------------|
| Objek yang dideteksi | Produk konsumer (botol, hp, buku) | TBS kelapa sawit |
| Model YOLO | Pretrained COCO (generik) | ❓ |
| Cara konfirmasi | Operator tekan SPACE | ❓ |
| Output data | CSV transaksi + struk | ❓ |
| Lingkungan | Indoor, cahaya normal | ❓ |
| Skala | 1 kasir, puluhan item/hari | ❓ |

**Pertanyaan:** Isi kolom "SawitVision (yang dibutuhkan)" berdasarkan analisis Anda.

---

### Bagian 2 — Eksperimen Sederhana (30 menit)

**Cari 3 foto TBS** dari sumber yang sah (Google Images, publikasi ilmiah, atau foto sendiri).

Pilih:
- 1 foto TBS matang (warna jingga/merah)
- 1 foto TBS mentah (warna hitam/hijau)
- 1 foto TBS yang sulit dinilai (campuran)

**Coba scan foto tersebut:**
```bash
python app.py --image foto_tbs_matang.jpg
```

**Catat hasil di tabel:**

| Foto | Objek Nyata | Terdeteksi sebagai | Conf | Relevan? |
|------|-------------|-------------------|------|----------|
| TBS Matang | Tandan buah | ??? | 0.__ | Ya/Tidak |
| TBS Mentah | Tandan buah | ??? | 0.__ | Ya/Tidak |
| TBS Sulit | Tandan buah | ??? | 0.__ | Ya/Tidak |

**Pertanyaan Kritis:**
> Model ini TIDAK mengenali TBS. Apakah ini kegagalan?  
> Atau justru ini adalah **pelajaran penting** tentang keterbatasan AI generik?  
> Jelaskan dalam 3–5 kalimat.

---

### Bagian 3 — Proposal Sistem (50 menit)

Buat proposal 1–2 halaman dengan struktur berikut:

#### 3.1 Problem Statement
Jelaskan masalah bisnis yang ingin diselesaikan:
- Apa yang terjadi jika grading TBS salah?
- Berapa estimasi kerugian per ton jika salah grade?
- Mengapa solusi manual tidak cukup?

#### 3.2 Proposed Solution
Gambar ulang skema sistem di atas dengan detail:
- Spesifikasi kamera yang cocok (IP camera, resolusi, posisi pemasangan)
- Tipe model AI yang dibutuhkan (pretrained vs custom)
- Bagaimana operator melakukan konfirmasi?
- Di mana data disimpan?

#### 3.3 Data Requirements
Sebutkan data yang harus dikumpulkan sebelum sistem bisa dibangun:

```
Minimal dataset untuk pilot:
  □ _____ foto TBS per kelas kematangan
  □ Label/anotasi oleh: _____________________
  □ Variasi kondisi: cahaya, sudut, cuaca
  □ Metadata wajib per foto: ________________
```

#### 3.4 Pilot KPI
Tentukan 3 KPI yang **bisa diukur** saat pilot:

| KPI | Cara Mengukur | Target Minimum |
|-----|---------------|----------------|
| Akurasi deteksi | | |
| Waktu per inspeksi | | |
| Tingkat override petugas | | |

> ⚠️ Jangan mengarang target tanpa dasar. Tuliskan: *"Target akan ditetapkan setelah baseline manual diukur."*

#### 3.5 Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|--------|--------|---------|
| Model salah grade TBS matang jadi mentah | | |
| Kamera rusak atau kotor | | |
| Petugas tidak percaya pada sistem AI | | |
| Data foto mengandung identitas pekerja | | |

#### 3.6 Roadmap Implementasi

```
Minggu 1–2:   Pengumpulan foto TBS berlabel (min. 200 foto/kelas)
Minggu 3–4:   Training model YOLO custom
Minggu 5:     Testing di laboratorium
Minggu 6–7:   Pilot di 1 loading ramp
Minggu 8:     Evaluasi dan keputusan scale-up
```

**Pertanyaan:** Apa risiko jika skip langsung ke Minggu 6 tanpa Minggu 1–5?

---

### Bagian 4 — Refleksi Etika (20 menit)

Jawab pertanyaan berikut:

**4.1 Hak Pekerja**
Kamera di loading ramp akan merekam aktivitas pekerja. Apa yang perlu dilakukan perusahaan sebelum memasang kamera?

**4.2 Akuntabilitas Keputusan**
Jika sistem AI salah grade dan perusahaan rugi, siapa yang bertanggung jawab: pengembang AI, operator yang konfirmasi, atau manajer yang memutuskan pakai sistem?

**4.3 Kepercayaan**
Petugas senior yang sudah 10 tahun grading TBS menolak sistem AI karena merasa tidak dipercaya. Bagaimana Anda mengelola perubahan ini?

---

## 📦 Output yang Dikumpulkan

```
sawit/
  proposal_sawitvision.pdf          ← Bagian 1–3 dalam format laporan
  tabel_eksperimen_tbs.pdf          ← Bagian 2 (tabel + analisis kritis)
  refleksi_etika.pdf                ← Bagian 4
  foto_tbs_1.jpg + foto_tbs_2.jpg   ← Foto yang digunakan (tanpa wajah pekerja)
  screenshot_scan_tbs.png           ← Hasil scan foto TBS di aplikasi
```

Masukkan ke dalam ZIP: `NamaNIM_SmartRetail.zip` → folder `sawit/`

---

## 🏆 Rubrik Penilaian Tugas Sawit

| Komponen | Bobot | Indikator Nilai Penuh |
|----------|-------|----------------------|
| Analisis gap (Bagian 1) | 20% | Tabel terisi lengkap + penjelasan logis |
| Eksperimen TBS (Bagian 2) | 20% | Foto diuji + analisis kritis mengapa model gagal |
| Proposal teknis (Bagian 3) | 40% | Problem clear, solusi realistis, KPI terukur, risiko lengkap |
| Refleksi etika (Bagian 4) | 20% | Jawaban substantif, bukan hanya formalitas |

---

## 📚 Referensi yang Bisa Digunakan

| Sumber | Topik | Link |
|--------|-------|------|
| Roboflow | Dataset TBS publik | https://roboflow.com |
| Ultralytics Docs | Fine-tuning YOLO | https://docs.ultralytics.com/modes/train |
| Kaggle | Palm Oil Dataset | https://kaggle.com |
| Jurnal | Computer Vision pertanian | Google Scholar: "oil palm bunch detection YOLO" |

---

> 💡 **Tips:** Proposal yang jujur tentang keterbatasan lebih bernilai  
> daripada proposal yang mengklaim AI bisa segalanya.  
> Manajer bisnis yang baik ingin tahu **apa yang tidak bisa dilakukan** sistem,  
> bukan hanya janji-janji optimis.

---

*Semangat! Industri sawit Indonesia membutuhkan inovator muda yang berpikir kritis.* 🌴
