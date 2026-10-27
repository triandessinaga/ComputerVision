# 📚 Teori: Computer Vision untuk Bisnis
### Referensi Akademik & Praktis

> Dokumen ini mendukung praktikum **Smart Retail Inspector** dan **Tugas SawitVision**.  
> Dibaca sebelum atau sesudah praktikum untuk memperdalam pemahaman konsep.

---

## 1. Apa Itu Computer Vision?

**Computer Vision** adalah cabang AI yang memungkinkan komputer "melihat" dan memahami
gambar atau video — sama seperti mata manusia, tetapi jauh lebih cepat dan konsisten.

### Analogi Sederhana

```
Manusia:   Mata → Otak → "Itu botol Aqua"
Komputer:  Kamera → Model AI → "bottle, confidence: 0.87"
```

Bedanya: manusia memahami konteks, AI hanya mengenali pola visual.

### Contoh Penerapan di Dunia Bisnis

| Industri | Penerapan | Manfaat |
|----------|-----------|---------|
| Retail | Deteksi produk di rak, kasir otomatis | Kurangi antrian, cegah shrinkage |
| Manufaktur | Inspeksi cacat produk | Kualitas konsisten, tanpa lelah |
| Pertanian | Deteksi kematangan buah, hama | Panen tepat waktu, kurangi losses |
| Logistik | Counting & sorting paket | Akurasi pengiriman lebih tinggi |
| Kesehatan | Deteksi anomali pada X-ray | Bantu dokter, percepat diagnosis |

---

## 2. Bagaimana YOLO Bekerja?

**YOLO** (You Only Look Once) adalah algoritma object detection yang memproses
seluruh gambar sekaligus dalam satu kali inferensi — itulah mengapa sangat cepat.

### Timeline Perkembangan YOLO

```
YOLOv1 (2016) → v2 → v3 → v4 → v5 → v8 → YOLO11 (2024)
     Makin cepat, makin akurat, makin ringan
```

### Proses Deteksi

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Input Image │────▶│  Neural Network  │────▶│  Output: Bounding   │
│  (frame)    │     │  (YOLO weights)  │     │  Box + Class + Conf │
└─────────────┘     └──────────────────┘     └─────────────────────┘
                           ▲
                    Dilatih dengan
                    jutaan gambar
                    (COCO Dataset)
```

### Komponen Output YOLO

| Komponen | Penjelasan | Contoh |
|----------|-----------|--------|
| **Bounding Box** | Koordinat kotak (x, y, width, height) | Posisi botol di frame |
| **Class** | Nama kategori objek | `bottle`, `book`, `person` |
| **Confidence** | Skor keyakinan 0–1 | `0.87` = 87% yakin |

### COCO Dataset — 80 Kategori

Model YOLO yang kita pakai dilatih dengan **COCO** (Common Objects in Context) —
dataset berisi 330.000+ gambar dengan 80 kategori benda sehari-hari.

Contoh kelas COCO yang relevan untuk retail:
`bottle`, `cup`, `book`, `cell phone`, `laptop`, `keyboard`, `mouse`,
`banana`, `apple`, `orange`, `carrot`, `scissors`, `clock`, `remote`

> **Keterbatasan:** COCO mengenali *kategori*, bukan *merek*.
> `bottle` = semua botol, tidak bisa bedakan Aqua vs Sprite.

**Referensi:**
- Lin, T.Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV 2014.
- https://cocodataset.org

---

## 3. Transfer Learning & Fine-Tuning

### Mengapa Tidak Latih dari Nol?

Melatih model dari awal butuh:
- Jutaan gambar berlabel
- Ratusan jam komputasi (GPU mahal)
- Keahlian deep learning tingkat lanjut

### Solusi: Transfer Learning

```
Model Pretrained              Fine-tuned Model
(COCO, 80 kelas)     ──────▶  (TBS Sawit, 3 kelas)
       │                            │
Sudah "mengerti"            Tambah pengetahuan
bentuk, tekstur,            khusus domain sawit
tepi, pola umum             dengan data yang lebih sedikit
```

Dengan transfer learning, kita bisa melatih model domain khusus
dengan **hanya 200–500 gambar** per kelas (vs jutaan dari scratch).

**Referensi:**
- Redmon, J., & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv:1804.02767
- Jocher, G., et al. (2023). *Ultralytics YOLOv8*. https://github.com/ultralytics/ultralytics
- https://docs.ultralytics.com/modes/train/

---

## 4. Human-in-the-Loop: Mengapa AI Tidak Boleh 100% Otomatis?

### Masalah dengan Otomasi Penuh

```
Skenario: AI langsung scan → langsung catat → langsung proses

Risiko:
  - laptop (Rp 5.499.000) terdeteksi sebagai book (Rp 7.500)
  - Selisih: Rp 5.491.500 per transaksi
  - 10 transaksi/hari × 250 hari = Rp 13.7 Milyar kerugian/tahun
```

### Model Human-in-the-Loop

```
AI Detection
     │
     ▼ (proposal)
Operator Review  ←── "Apakah ini benar?"
     │
     ▼ (konfirmasi)
Data Recorded
```

Dalam aplikasi kita: AI mendeteksi → Anda lihat hasilnya → baru tekan `SPACE`.

### Kapan AI Bisa Dipercaya Lebih?

| Kondisi | Trust Level | Alasan |
|---------|-------------|--------|
| Confidence > 0.90, produk simpel | Tinggi | Pola visual jelas |
| Confidence 0.50–0.90 | Sedang | Perlu konfirmasi |
| Confidence < 0.50 | Rendah | Kemungkinan salah besar |
| Lingkungan tidak familiar | Rendah | Distribusi berbeda dari training |

**Referensi:**
- Amershi, S., et al. (2019). *Software Engineering for Machine Learning*. ICSE 2019.
- Cai, C.J., et al. (2019). *Human-Centered Tools for Coping with Imperfect Algorithms*. CHI 2019.

---

## 5. Computer Vision untuk Industri Kelapa Sawit

### Tantangan Industri

Indonesia adalah **produsen CPO terbesar di dunia** (± 47 juta ton/tahun).
Kualitas CPO sangat bergantung pada ketepatan grading TBS di loading ramp.

**Masalah grading manual:**
- Subjektif — petugas berbeda bisa beda keputusan
- Lambat — bottle-neck di loading ramp
- Tidak konsisten antar shift (pagi vs malam)
- Tidak ada data digital untuk analisis

### Kelas Kematangan TBS

| Kelas | Visual | Implikasi Bisnis |
|-------|--------|-----------------|
| **Unripe (Mentah)** | Warna hitam/hijau, brondolan < 2 | Kandungan minyak rendah, harga rendah |
| **Ripe (Matang)** | Warna jingga/merah, brondolan berjatuhan | Kandungan minyak optimal, harga terbaik |
| **Overripe (Lewat Matang)** | Brondolan banyak jatuh, warna gelap | Asam lemak bebas (ALB) tinggi, kualitas turun |

### Dataset Publik TBS untuk Belajar

| Dataset | Platform | Kelas | Jumlah Gambar |
|---------|----------|-------|---------------|
| Oil Palm Fresh Fruit Bunch | Roboflow Universe | 3 kelas | 1.200+ |
| Palm Oil Detection | Kaggle | 2 kelas | 800+ |
| SPOC Dataset | Zenodo | 4 kelas | 2.500+ |

**Cara akses Roboflow:**
1. Buka https://universe.roboflow.com
2. Search: `oil palm bunch` atau `TBS sawit`
3. Pilih dataset → Export → Format: YOLOv8

**Referensi:**
- Shafii, S., et al. (2021). *Oil Palm Fresh Fruit Bunch Ripeness Classification*. IEEE Access.
- Dwiputra, R., et al. (2022). *YOLO-based Oil Palm Bunch Detection*. Jurnal Teknologi, 84(4).
- Roboflow Universe: https://universe.roboflow.com/search?q=oil+palm
- Ultralytics Fine-tuning: https://docs.ultralytics.com/modes/train/

---

## 6. Arsitektur Sistem AI untuk Bisnis

### Komponen Sistem Lengkap

```
┌────────────────────────────────────────────────────────────────┐
│                    SISTEM AI BISNIS                            │
│                                                                │
│  INPUT         PROCESSING          OUTPUT          IMPACT      │
│  ─────         ──────────          ──────          ──────      │
│  Kamera   →   Preprocessing  →   Detection   →   Business     │
│  Sensor        (resize,            (YOLO)         Decision     │
│  Data           normalize)            │                        │
│                                       ▼                        │
│                              Human Validation                  │
│                                       │                        │
│                                       ▼                        │
│                               Database / CSV                   │
│                                       │                        │
│                                       ▼                        │
│                              Dashboard / Report                │
└────────────────────────────────────────────────────────────────┘
```

### Pertanyaan Bisnis Sebelum Implementasi AI

Sebelum adopt AI, jawab dulu:
1. **Problem:** Masalah bisnis apa yang diselesaikan?
2. **Data:** Data apa yang tersedia dan berkualitas?
3. **Accuracy:** Seberapa akurat yang cukup untuk bisnis ini?
4. **Cost:** Berapa biaya implementasi vs manfaat?
5. **Risk:** Apa konsekuensi jika AI salah?
6. **Ethics:** Siapa yang terdampak? Apakah ada bias?

---

## 7. Metrik Evaluasi Model

### Confusion Matrix

```
                    Prediksi AI
                  Positif  Negatif
Aktual  Positif │   TP   │   FN  │
        Negatif │   FP   │   TN  │
```

### Metrik Penting

| Metrik | Formula | Artinya |
|--------|---------|---------|
| **Accuracy** | (TP+TN) / Total | Seberapa sering benar secara keseluruhan |
| **Precision** | TP / (TP+FP) | Dari yang diprediksi positif, berapa yang benar? |
| **Recall** | TP / (TP+FN) | Dari yang benar positif, berapa yang terdeteksi? |
| **F1-Score** | 2 × (P×R)/(P+R) | Keseimbangan precision dan recall |
| **mAP** | Mean Average Precision | Metrik standar object detection |

### Mana yang Lebih Penting?

Tergantung konteks bisnis:
- **Inspeksi TBS:** Recall lebih penting — lebih baik over-detect daripada miss TBS matang
- **Fraud detection:** Precision lebih penting — false alarm mahal secara operasional

---

## 8. Privasi & Etika AI

### Prinsip Dasar

| Prinsip | Penjelasan | Contoh Kasir AI |
|---------|-----------|----------------|
| **Minimisasi Data** | Kumpulkan hanya yang perlu | Foto produk, bukan wajah pelanggan |
| **Transparansi** | Beritahu yang terdampak | Kasir tahu sistem merekam |
| **Akuntabilitas** | Ada yang bertanggung jawab | Manajer tanda tangani kebijakan |
| **Non-diskriminasi** | AI tidak boleh bias | Deteksi tidak berdasarkan ras/gender |

### Regulasi Relevan

- **UU PDP (2022)** — Undang-Undang Perlindungan Data Pribadi Indonesia
- **GDPR (2018)** — General Data Protection Regulation (EU, referensi global)

**Referensi:**
- Floridi, L., et al. (2018). *AI4People—An Ethical Framework for a Good AI Society*. Minds and Machines, 28(4).
- https://www.kominfo.go.id/uu-pdp

---

## 📚 Daftar Referensi Lengkap

### Buku
1. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow* (3rd ed.). O'Reilly.
2. Howard, J., & Gugger, S. (2020). *Deep Learning for Coders with fastai & PyTorch*. O'Reilly.
3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.

### Paper
4. Redmon, J., et al. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. CVPR 2016.
5. Lin, T.Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV 2014.
6. Shafii, S., et al. (2021). *Deep Learning for Oil Palm TBS Ripeness*. IEEE Access, 9.

### Online Resources
7. Ultralytics YOLO Docs: https://docs.ultralytics.com
8. Roboflow Universe (dataset): https://universe.roboflow.com
9. Kaggle Datasets: https://kaggle.com/datasets
10. OpenCV Documentation: https://docs.opencv.org

---

*Dibuat untuk mendukung praktikum AI untuk Bisnis — Sistem Informasi*  
*© 2026 Triandes Sinaga*
