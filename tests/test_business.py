"""
Unit Test — Smart Retail Inspector
Jalankan: python -m pytest tests/ -v
         atau: python -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

# Tambahkan root project ke path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import CATALOG, load_catalog, rupiah, hitung_pecahan, save_inspection_csv


# ── Test Katalog ───────────────────────────────────────────────────────────────
class TestCatalog(unittest.TestCase):

    def test_catalog_not_empty(self):
        """Katalog harus berisi minimal 1 produk."""
        self.assertGreater(len(CATALOG), 0)

    def test_all_prices_positive(self):
        """Semua harga harus > 0."""
        for label, item in CATALOG.items():
            with self.subTest(label=label):
                self.assertGreater(item["price_idr"], 0,
                    f"Harga {label} harus positif")

    def test_all_have_required_fields(self):
        """Setiap produk harus punya 'product' dan 'price_idr'."""
        for label, item in CATALOG.items():
            with self.subTest(label=label):
                self.assertIn("product", item)
                self.assertIn("price_idr", item)

    def test_no_comment_keys(self):
        """Key yang diawali '_' (komentar) tidak boleh masuk CATALOG."""
        for key in CATALOG:
            self.assertFalse(key.startswith("_"),
                f"Key '{key}' seharusnya dibuang saat load")

    def test_known_yolo_classes_in_catalog(self):
        """Minimal kelas umum COCO seperti bottle dan book harus ada."""
        for cls in ["bottle", "book"]:
            self.assertIn(cls, CATALOG,
                f"YOLO class '{cls}' harus ada di katalog")


# ── Test Format Rupiah ─────────────────────────────────────────────────────────
class TestRupiah(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(rupiah(12000), "Rp 12.000")

    def test_million(self):
        self.assertEqual(rupiah(1000000), "Rp 1.000.000")

    def test_zero(self):
        self.assertEqual(rupiah(0), "Rp 0")

    def test_large(self):
        self.assertEqual(rupiah(6500000), "Rp 6.500.000")


# ── Test Kalkulator Kembalian ──────────────────────────────────────────────────
class TestPecahan(unittest.TestCase):

    def test_exact_no_change(self):
        """Bayar pas — kembalian 0, tidak ada pecahan."""
        self.assertEqual(hitung_pecahan(0), {})

    def test_simple_change(self):
        """Kembalian 5000 = 1 lembar 5000."""
        result = hitung_pecahan(5000)
        self.assertEqual(result.get(5000), 1)

    def test_complex_change(self):
        """Kembalian 87300 = 50000+20000+10000+5000+2000+200+100."""
        result = hitung_pecahan(87300)
        total  = sum(p * j for p, j in result.items())
        self.assertEqual(total, 87300, "Total pecahan harus sama dengan kembalian")

    def test_all_pecahan_keys_valid(self):
        """Semua key pecahan harus nilai uang yang valid."""
        valid = {100000,50000,20000,10000,5000,2000,1000,500,200,100}
        for p in hitung_pecahan(99999):
            self.assertIn(p, valid)

    def test_sum_equals_input(self):
        """Untuk berbagai nilai, sum(pecahan) == input."""
        for amount in [100, 500, 3500, 27500, 150000, 999900]:
            with self.subTest(amount=amount):
                result = hitung_pecahan(amount)
                total  = sum(p * j for p, j in result.items())
                self.assertEqual(total, amount)


# ── Test Filter Catalog (hanya kelas yang ada di CATALOG) ─────────────────────
class TestCatalogFilter(unittest.TestCase):

    def _filter(self, detections):
        """Simulasi filter: hanya kembalikan deteksi yang ada di CATALOG."""
        return [(label, score) for label, score in detections if label in CATALOG]

    def test_known_only(self):
        result = self._filter([("bottle", 0.9), ("person", 0.8)])
        self.assertEqual(result, [("bottle", 0.9)])

    def test_empty_if_none_known(self):
        result = self._filter([("person", 0.95), ("car", 0.80)])
        self.assertEqual(result, [])

    def test_multiple_known(self):
        result = self._filter([("book", 0.7), ("cup", 0.6), ("chair", 0.5)])
        labels = [r[0] for r in result]
        self.assertIn("book", labels)
        self.assertIn("cup", labels)
        self.assertNotIn("chair", labels)

    def test_preserves_confidence(self):
        result = self._filter([("bottle", 0.92)])
        self.assertAlmostEqual(result[0][1], 0.92)


if __name__ == "__main__":
    unittest.main(verbosity=2)
