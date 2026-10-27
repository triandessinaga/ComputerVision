"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              SMART RETAIL INSPECTOR  v2.0                                   ║
║              AI-Powered Product Detection • Light Modern GUI                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Keyboard Shortcuts (fokus di jendela utama):                               ║
║    SPACE  → Tambah produk terdeteksi ke keranjang (+1)                      ║
║    TAB    → Ganti pilihan deteksi (jika ada lebih dari 1)                   ║
║    U      → Undo item terakhir dari keranjang                               ║
║    C      → Checkout / bayar                                                ║
║    N      → Reset keranjang (New transaction)                               ║
║    S      → Simpan inspeksi ke CSV (tanpa checkout)                         ║
║    Q / Esc→ Keluar aplikasi                                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

Cara jalankan:
    python app.py                      # webcam default
    python app.py --camera 1           # webcam ke-2
    python app.py --image foto.jpg     # mode gambar statis (fallback)
    python app.py --conf 0.35          # turunkan threshold deteksi
"""

import argparse
import csv
import json
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
from datetime import datetime
from pathlib import Path

# ── Optional imports (graceful fallback) ──────────────────────────────────────
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT         = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "data" / "catalog.json"
OUTPUT_DIR   = ROOT / "output"
MODEL_PATH   = ROOT / "yolo11n.pt"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Load catalog ───────────────────────────────────────────────────────────────
def load_catalog() -> dict:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    # Buang key komentar
    return {k: v for k, v in raw.items() if not k.startswith("_")}

CATALOG = load_catalog()

# ── Kelas YOLO yang TIDAK boleh ditambah ke keranjang ─────────────────────────
# Meskipun YOLO mendeteksi kelas ini, sistem akan mengabaikannya.
YOLO_BLACKLIST = {
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "microwave",
    "oven", "toaster", "sink", "refrigerator", "hair drier", "toothbrush",
    "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "wine glass", "handbag", "umbrella", "backpack",
}

# ── Color Palette — Light Modern ───────────────────────────────────────────────
C = {
    "bg":           "#F0F4F8",
    "surface":      "#FFFFFF",
    "topbar":       "#FFFFFF",
    "primary":      "#2563EB",
    "primary_lt":   "#DBEAFE",
    "primary_dk":   "#1D4ED8",
    "success":      "#16A34A",
    "success_lt":   "#DCFCE7",
    "danger":       "#DC2626",
    "danger_lt":    "#FEE2E2",
    "warning":      "#D97706",
    "warning_lt":   "#FEF3C7",
    "info":         "#0891B2",
    "info_lt":      "#CFFAFE",
    "text":         "#0F172A",
    "text2":        "#475569",
    "text3":        "#94A3B8",
    "border":       "#E2E8F0",
    "row_even":     "#FFFFFF",
    "row_odd":      "#F8FAFC",
    "row_sel":      "#DBEAFE",
    "row_sel_fg":   "#1E40AF",
    "kbd_bg":       "#F1F5F9",
    "kbd_border":   "#CBD5E1",
}

FF = "Segoe UI"
def fnt(size=10, w="normal"): return (FF, size, w)

# ── Helpers ────────────────────────────────────────────────────────────────────
def rupiah(v: int) -> str:
    return "Rp {:,}".format(int(v)).replace(",", ".")

def hitung_pecahan(n: int) -> dict:
    pecahan = [100000,50000,20000,10000,5000,2000,1000,500,200,100]
    hasil, sisa = {}, n
    for p in pecahan:
        j = sisa // p
        if j: hasil[p] = j
        sisa -= j * p
    return hasil

def save_inspection_csv(label: str, conf: float, source: str,
                         sample_id: str, qty: int = 1,
                         annotated_frame=None) -> Path:
    """
    Simpan satu baris inspeksi yang sudah diverifikasi operator.
    - qty         : jumlah unit yang disimpan
    - annotated_frame : frame BGR yang sudah ada bounding box YOLO (bukan raw)
    """
    item       = CATALOG[label]
    unit_price = item["price_idr"]
    subtotal   = unit_price * qty
    stamp      = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    img_file   = ""

    # Simpan gambar yang SUDAH di-annotate (ada bounding box)
    if annotated_frame is not None and HAS_CV2:
        img_path = OUTPUT_DIR / f"{stamp}_annotated.jpg"
        cv2.imwrite(str(img_path), annotated_frame)
        img_file = img_path.name

    path   = OUTPUT_DIR / "inspections.csv"
    is_new = not path.exists() or path.stat().st_size == 0
    fields = ["timestamp", "sample_id", "source", "yolo_class", "sku",
              "product", "category", "qty", "unit_price_idr", "subtotal_idr",
              "confidence", "operator_confirmed", "image_file"]
    with path.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if is_new:
            w.writeheader()
        w.writerow({
            "timestamp":          datetime.now().isoformat(timespec="seconds"),
            "sample_id":          sample_id,
            "source":             source,
            "yolo_class":         label,
            "sku":                item.get("sku", ""),
            "product":            item["product"],
            "category":           item.get("category", ""),
            "qty":                qty,
            "unit_price_idr":     unit_price,
            "subtotal_idr":       subtotal,
            "confidence":         f"{conf:.3f}",
            "operator_confirmed": "YES",
            "image_file":         img_file,
        })
    return path

def save_transaction_csv(cart: dict, bayar: int, kasir: str) -> tuple:
    """Simpan transaksi checkout ke output/transactions.csv + struk .txt"""
    total     = sum(i["price"] * i["qty"] for i in cart.values())
    kembalian = bayar - total
    now       = datetime.now()
    invoice   = now.strftime("INV-%Y%m%d-%H%M%S-%f")
    receipts  = OUTPUT_DIR / "receipts"
    receipts.mkdir(exist_ok=True)
    # Struk
    lines = [
        "=" * 44,
        f"{'SMART RETAIL INSPECTOR':^44}",
        f"{'Demo Praktikum — BUKAN Struk Fiskal':^44}",
        "=" * 44,
        f"Invoice : {invoice}",
        f"Kasir   : {kasir}",
        f"Waktu   : {now.strftime('%d/%m/%Y %H:%M:%S')}",
        "-" * 44,
        f"{'Produk':<22}{'Qty':>4}{'Harga':>9}{'Sub':>9}",
        "-" * 44,
    ]
    for item in cart.values():
        sub = item["price"] * item["qty"]
        lines.append(f"{item['name'][:21]:<22}{item['qty']:>4}"
                     f"{rupiah(item['price']):>9}{rupiah(sub):>9}")
    lines += [
        "-" * 44,
        f"{'TOTAL':<32}{rupiah(total):>12}",
        f"{'BAYAR':<32}{rupiah(bayar):>12}",
        f"{'KEMBALIAN':<32}{rupiah(kembalian):>12}",
        "=" * 44,
        f"{'Terima kasih!':^44}",
        "=" * 44, "",
    ]
    receipt_path = receipts / f"{invoice}.txt"
    receipt_path.write_text("\n".join(lines), encoding="utf-8")
    # CSV transaksi
    tx_path = OUTPUT_DIR / "transactions.csv"
    is_new  = not tx_path.exists() or tx_path.stat().st_size == 0
    with tx_path.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["invoice","timestamp","kasir","sku","product",
                        "qty","unit_price","line_total","payment","change"])
        for item in cart.values():
            w.writerow([invoice, now.isoformat(timespec="seconds"), kasir,
                        item["sku"], item["name"], item["qty"], item["price"],
                        item["price"]*item["qty"], bayar, kembalian])
    return invoice, receipt_path, kembalian


# ══════════════════════════════════════════════════════════════════════════════
#  WIDGET LIBRARY
# ══════════════════════════════════════════════════════════════════════════════
class Card(tk.Frame):
    def __init__(self, master, **kw):
        kw.setdefault("bg", C["surface"]); kw.setdefault("padx",14); kw.setdefault("pady",10)
        super().__init__(master, relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=C["border"], **kw)

class KbdHint(tk.Label):
    """Tombol keyboard visual  [SPACE]"""
    def __init__(self, master, key, desc="", **kw):
        kw.setdefault("bg", C["bg"])
        frame = tk.Frame(master, bg=kw["bg"])
        # kotak tombol
        self._key_lbl = tk.Label(frame, text=f" {key} ",
                                  font=("Consolas", 9, "bold"),
                                  bg=C["kbd_bg"], fg=C["text"],
                                  relief="flat", bd=0,
                                  highlightthickness=1,
                                  highlightbackground=C["kbd_border"],
                                  padx=4, pady=1)
        self._key_lbl.pack(side="left")
        if desc:
            tk.Label(frame, text=f" {desc}", font=fnt(8),
                     bg=kw["bg"], fg=C["text2"]).pack(side="left")
        self._frame = frame
        super().__init__(master, **kw)

    def pack(self, **kw):
        self._frame.pack(**kw)

    def grid(self, **kw):
        self._frame.grid(**kw)

class PrimaryBtn(tk.Button):
    def __init__(self, m, **kw):
        kw.setdefault("font",fnt(10,"bold")); kw.setdefault("bg",C["primary"])
        kw.setdefault("fg","#FFF"); kw.setdefault("activebackground",C["primary_dk"])
        kw.setdefault("activeforeground","#FFF"); kw.setdefault("relief","flat")
        kw.setdefault("bd",0); kw.setdefault("cursor","hand2")
        kw.setdefault("padx",16); kw.setdefault("pady",8)
        super().__init__(m,**kw)

class SecondaryBtn(tk.Button):
    def __init__(self, m, **kw):
        kw.setdefault("font",fnt(9,"bold")); kw.setdefault("bg",C["kbd_bg"])
        kw.setdefault("fg",C["text"]); kw.setdefault("activebackground",C["border"])
        kw.setdefault("relief","flat"); kw.setdefault("bd",0)
        kw.setdefault("cursor","hand2"); kw.setdefault("padx",12); kw.setdefault("pady",6)
        super().__init__(m,**kw)

class DangerBtn(tk.Button):
    def __init__(self, m, **kw):
        kw.setdefault("font",fnt(9,"bold")); kw.setdefault("bg",C["danger_lt"])
        kw.setdefault("fg",C["danger"]); kw.setdefault("activebackground","#FECACA")
        kw.setdefault("relief","flat"); kw.setdefault("bd",0)
        kw.setdefault("cursor","hand2"); kw.setdefault("padx",12); kw.setdefault("pady",6)
        super().__init__(m,**kw)

class SuccessBtn(tk.Button):
    def __init__(self, m, **kw):
        kw.setdefault("font",fnt(12,"bold")); kw.setdefault("bg",C["success"])
        kw.setdefault("fg","#FFF"); kw.setdefault("activebackground","#15803D")
        kw.setdefault("activeforeground","#FFF"); kw.setdefault("relief","flat")
        kw.setdefault("bd",0); kw.setdefault("cursor","hand2"); kw.setdefault("pady",13)
        super().__init__(m,**kw)

class Divider(tk.Frame):
    def __init__(self, m, **kw):
        kw.setdefault("bg",C["border"]); kw.setdefault("height",1)
        super().__init__(m,**kw)

class Badge(tk.Label):
    def __init__(self, m, text, color=None, fg=None, **kw):
        kw.setdefault("font",fnt(8,"bold")); kw.setdefault("padx",8); kw.setdefault("pady",2)
        super().__init__(m, text=text, bg=color or C["primary_lt"],
                         fg=fg or C["primary"], relief="flat", bd=0, **kw)


# ══════════════════════════════════════════════════════════════════════════════
#  DIALOG CHECKOUT
# ══════════════════════════════════════════════════════════════════════════════
class CheckoutDialog(tk.Toplevel):
    def __init__(self, parent, cart: dict, kasir: str, on_success):
        super().__init__(parent)
        self.cart       = cart
        self.kasir      = kasir
        self.on_success = on_success
        self.total      = sum(i["price"]*i["qty"] for i in cart.values())
        self.title("💳  Checkout — Pembayaran")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        self._center(520, 640)
        self._build()

    def _center(self, w, h):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width()-w)//2
        y = self.master.winfo_rooty() + (self.master.winfo_height()-h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=C["primary"], pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="💳  Pembayaran Transaksi",
                 font=fnt(13,"bold"), bg=C["primary"], fg="#FFF").pack()
        tk.Label(hdr, text="Masukkan uang yang diterima dari pelanggan",
                 font=fnt(9), bg=C["primary"], fg="#BFDBFE").pack()

        body = tk.Frame(self, bg=C["bg"], padx=18, pady=10)
        body.pack(fill="both", expand=True)

        # Ringkasan
        tk.Label(body, text="RINGKASAN BELANJA", font=fnt(8,"bold"),
                 bg=C["bg"], fg=C["text3"]).pack(anchor="w", pady=(0,4))
        tbl = Card(body, padx=0, pady=0)
        tbl.pack(fill="x", pady=(0,10))
        hrow = tk.Frame(tbl, bg=C["primary_lt"])
        hrow.pack(fill="x")
        for txt, anc, w in [("Produk","w",24),("Qty","center",4),("Subtotal","e",12)]:
            tk.Label(hrow, text=txt, font=fnt(8,"bold"), bg=C["primary_lt"],
                     fg=C["primary"], anchor=anc, padx=8, pady=5,
                     width=w).pack(side="left")
        for i, item in enumerate(self.cart.values()):
            sub   = item["price"]*item["qty"]
            bg    = C["row_even"] if i%2==0 else C["row_odd"]
            row   = tk.Frame(tbl, bg=bg)
            row.pack(fill="x")
            tk.Label(row, text=item["name"][:24], font=fnt(9), bg=bg,
                     fg=C["text"], anchor="w", padx=8, pady=4, width=24).pack(side="left")
            tk.Label(row, text=str(item["qty"]), font=fnt(9), bg=bg,
                     fg=C["text2"], anchor="center", width=5).pack(side="left")
            tk.Label(row, text=rupiah(sub), font=fnt(9,"bold"), bg=bg,
                     fg=C["text"], anchor="e", padx=8, width=14).pack(side="right")

        # Total
        tot_card = Card(body, bg=C["primary_lt"], padx=14, pady=10)
        tot_card.pack(fill="x", pady=(0,12))
        tr = tk.Frame(tot_card, bg=C["primary_lt"])
        tr.pack(fill="x")
        tk.Label(tr, text="TOTAL", font=fnt(10,"bold"),
                 bg=C["primary_lt"], fg=C["primary"]).pack(side="left")
        tk.Label(tr, text=rupiah(self.total), font=fnt(17,"bold"),
                 bg=C["primary_lt"], fg=C["primary"]).pack(side="right")

        # Input bayar
        tk.Label(body, text="JUMLAH UANG DITERIMA (Rp)",
                 font=fnt(8,"bold"), bg=C["bg"], fg=C["text3"]).pack(anchor="w",pady=(0,4))
        ef = tk.Frame(body, bg=C["surface"], highlightthickness=2,
                      highlightbackground=C["primary"])
        ef.pack(fill="x", pady=(0,8))
        tk.Label(ef, text="Rp", font=fnt(13,"bold"), bg=C["surface"],
                 fg=C["text3"], padx=10).pack(side="left")
        self.var_bayar = tk.StringVar()
        self.var_bayar.trace_add("write", self._on_change)
        entry = tk.Entry(ef, textvariable=self.var_bayar, font=fnt(17,"bold"),
                         bg=C["surface"], fg=C["text"], insertbackground=C["primary"],
                         relief="flat", bd=0)
        entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0,10))
        entry.focus_set()

        # Nominal cepat
        qf = tk.Frame(body, bg=C["bg"])
        qf.pack(fill="x", pady=(0,8))
        for amt in [5000,10000,20000,50000,100000]:
            SecondaryBtn(qf, text=f"+{rupiah(amt)}", font=fnt(8,"bold"),
                         command=lambda a=amt: self._add(a)).pack(side="left",padx=(0,4))
        PrimaryBtn(qf, text="Uang Pas", font=fnt(8,"bold"), pady=6, padx=10,
                   command=lambda: self.var_bayar.set(str(self.total))).pack(side="left")

        Divider(body).pack(fill="x", pady=8)

        # Kembalian
        km = Card(body, bg=C["success_lt"], padx=14, pady=10)
        km.pack(fill="x", pady=(0,4))
        kr = tk.Frame(km, bg=C["success_lt"])
        kr.pack(fill="x")
        tk.Label(kr, text="KEMBALIAN", font=fnt(10,"bold"),
                 bg=C["success_lt"], fg=C["success"]).pack(side="left")
        self.lbl_kem = tk.Label(kr, text="Rp 0", font=fnt(17,"bold"),
                                 bg=C["success_lt"], fg=C["success"])
        self.lbl_kem.pack(side="right")
        self.lbl_pec = tk.Label(body, text="", font=fnt(8),
                                 bg=C["bg"], fg=C["text2"], anchor="w")
        self.lbl_pec.pack(fill="x", pady=(4,2))
        self.lbl_err = tk.Label(body, text="", font=fnt(9,"bold"),
                                 bg=C["bg"], fg=C["danger"])
        self.lbl_err.pack(anchor="w")

        # Tombol
        bf = tk.Frame(self, bg=C["bg"], padx=18, pady=12)
        bf.pack(fill="x")
        SecondaryBtn(bf, text="✕  Batal", command=self.destroy).pack(side="left")
        SuccessBtn(bf, text="✓  PROSES PEMBAYARAN",
                   command=self._proses).pack(side="right",fill="x",expand=True,padx=(8,0))
        self.bind("<Return>", lambda e: self._proses())
        self.bind("<Escape>", lambda e: self.destroy())

    def _add(self, a):
        try: cur = int(self.var_bayar.get().replace(".","").replace(",",""))
        except: cur = 0
        self.var_bayar.set(str(cur+a))

    def _get_int(self):
        try: return int(self.var_bayar.get().replace(".","").replace(",","").strip())
        except: return 0

    def _on_change(self, *_):
        bayar     = self._get_int()
        kembalian = bayar - self.total
        if kembalian < 0:
            self.lbl_kem.config(text=rupiah(abs(kembalian)), fg=C["danger"])
            self.lbl_kem.master.config(bg=C["danger_lt"])
            self.lbl_err.config(text=f"⚠  Kurang {rupiah(abs(kembalian))}")
            self.lbl_pec.config(text="")
        else:
            self.lbl_kem.config(text=rupiah(kembalian), fg=C["success"])
            self.lbl_kem.master.config(bg=C["success_lt"])
            self.lbl_err.config(text="")
            pec = hitung_pecahan(kembalian)
            self.lbl_pec.config(
                text="Pecahan: " + "  ·  ".join(f"{rupiah(p)}×{j}" for p,j in pec.items())
                if pec else "")

    def _proses(self):
        bayar = self._get_int()
        if bayar < self.total:
            self.lbl_err.config(text=f"⚠  Uang kurang {rupiah(self.total-bayar)}")
            return
        invoice, path, kembalian = save_transaction_csv(self.cart, bayar, self.kasir)
        self.destroy()
        self.on_success(invoice, path, kembalian, bayar)


# ══════════════════════════════════════════════════════════════════════════════
#  DIALOG STRUK
# ══════════════════════════════════════════════════════════════════════════════
class ReceiptDialog(tk.Toplevel):
    def __init__(self, parent, invoice, path, kembalian, bayar, total):
        super().__init__(parent)
        self.title("✓  Transaksi Berhasil")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        w,h = 460,560
        x = parent.winfo_rootx()+(parent.winfo_width()-w)//2
        y = parent.winfo_rooty()+(parent.winfo_height()-h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self._build(invoice, path, kembalian, bayar, total)

    def _build(self, invoice, path, kembalian, bayar, total):
        tk.Frame(self, bg=C["success"], pady=18).pack(fill="x")
        banner = self.children[list(self.children)[-1]]
        tk.Label(banner, text="✓", font=fnt(26,"bold"),
                 bg=C["success"], fg="#FFF").pack()
        tk.Label(banner, text="Pembayaran Berhasil!",
                 font=fnt(12,"bold"), bg=C["success"], fg="#FFF").pack()
        tk.Label(banner, text=f"Kembalian  {rupiah(kembalian)}",
                 font=fnt(10), bg=C["success"], fg="#D1FAE5").pack(pady=(4,0))

        body = tk.Frame(self, bg=C["bg"], padx=20, pady=12)
        body.pack(fill="both", expand=True)

        for lbl,val,clr in [("Invoice",invoice,C["text"]),
                             ("Total",rupiah(total),C["warning"]),
                             ("Dibayar",rupiah(bayar),C["text"]),
                             ("Kembalian",rupiah(kembalian),C["success"])]:
            r = tk.Frame(body, bg=C["bg"]); r.pack(fill="x", pady=3)
            tk.Label(r,text=lbl,font=fnt(9),bg=C["bg"],fg=C["text2"]).pack(side="left")
            tk.Label(r,text=val,font=fnt(9,"bold"),bg=C["bg"],fg=clr).pack(side="right")

        if kembalian > 0:
            Divider(body).pack(fill="x", pady=8)
            tk.Label(body, text="Pecahan kembalian", font=fnt(8,"bold"),
                     bg=C["bg"], fg=C["text3"]).pack(anchor="w")
            pf = Card(body, padx=10, pady=6)
            pf.pack(fill="x", pady=(4,0))
            for p,j in hitung_pecahan(kembalian).items():
                r = tk.Frame(pf, bg=C["surface"]); r.pack(fill="x", pady=1)
                tk.Label(r,text=f"{rupiah(p)} × {j}",font=fnt(9),
                         bg=C["surface"],fg=C["text"]).pack(side="left")
                tk.Label(r,text=rupiah(p*j),font=fnt(9,"bold"),
                         bg=C["surface"],fg=C["text2"]).pack(side="right")

        Divider(body).pack(fill="x", pady=10)
        tk.Label(body, text="Preview Struk", font=fnt(8,"bold"),
                 bg=C["bg"], fg=C["text3"]).pack(anchor="w")
        tw = tk.Frame(body, bg=C["surface"],
                      highlightthickness=1, highlightbackground=C["border"])
        tw.pack(fill="both", expand=True, pady=(4,8))
        sb = tk.Scrollbar(tw, width=12)
        sb.pack(side="right", fill="y")
        txt = tk.Text(tw, font=("Consolas",8), bg=C["surface"], fg=C["text"],
                      relief="flat", bd=0, wrap="none", yscrollcommand=sb.set, height=8)
        txt.pack(side="left", fill="both", expand=True, padx=6)
        sb.config(command=txt.yview)
        txt.insert("end", path.read_text(encoding="utf-8"))
        txt.config(state="disabled")
        tk.Label(body, text=f"📄  {path.parent.name}/{path.name}",
                 font=fnt(8), bg=C["bg"], fg=C["text3"]).pack(anchor="w")
        PrimaryBtn(body, text="Transaksi Baru  →",
                   command=self.destroy).pack(fill="x", pady=(10,0))
        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())


# ══════════════════════════════════════════════════════════════════════════════
#  APLIKASI UTAMA
# ══════════════════════════════════════════════════════════════════════════════
class RetailInspectorApp(tk.Tk):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.title("Smart Retail Inspector  v2.0")
        self.configure(bg=C["bg"])
        self.minsize(1200, 720)
        self.state("zoomed")

        # State data
        self.cart         = {}           # {sku: {name, price, sku, qty}}
        self.undo_stack   = deque(maxlen=20)
        self.kasir        = "OPERATOR-01"
        self.sample_id    = "ITEM-001"
        self._sample_no   = 1

        # CV state
        self._cv_running   = False
        self._cv_cap       = None
        self._cv_model     = None
        self._cv_frame     = None         # raw BGR frame
        self._cv_annotated = None         # BGR frame dengan bounding box YOLO
        self._cv_pil       = None         # annotated PIL image untuk canvas
        self._cv_detects   = []           # [(label, conf), ...]
        self._cv_sel       = 0            # index deteksi terpilih
        self._cv_thread    = None
        self._cv_tk_img    = None
        self._cv_lock      = threading.Lock()

        self._sort_state  = {}

        self._setup_styles()
        self._build_ui()
        self._bind_keys()
        self._tick()

    # ── ttk styles ────────────────────────────────────────────────────────────
    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview", background=C["surface"], foreground=C["text"],
                    fieldbackground=C["surface"], rowheight=28,
                    font=fnt(9), borderwidth=0, relief="flat")
        s.configure("Treeview.Heading", background=C["primary_lt"],
                    foreground=C["primary"], font=fnt(9,"bold"),
                    relief="flat", borderwidth=0, padding=(8,5))
        s.map("Treeview",
              background=[("selected",C["row_sel"])],
              foreground=[("selected",C["row_sel_fg"])])
        s.configure("Vertical.TScrollbar", background=C["border"],
                    troughcolor=C["bg"], arrowcolor=C["text3"],
                    relief="flat", borderwidth=0)
        s.configure("TNotebook", background=C["bg"], borderwidth=0)
        s.configure("TNotebook.Tab", background=C["bg"], foreground=C["text2"],
                    font=fnt(9,"bold"), padding=(16,8), borderwidth=0)
        s.map("TNotebook.Tab",
              background=[("selected",C["surface"])],
              foreground=[("selected",C["primary"])],
              expand=[("selected",[1,1,1,0])])
        s.configure("TCombobox", fieldbackground=C["surface"],
                    background=C["surface"], foreground=C["text"],
                    selectbackground=C["primary_lt"])

    # ── Top bar ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        topbar = tk.Frame(self, bg=C["topbar"], height=58,
                          highlightthickness=1, highlightbackground=C["border"])
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # Logo kiri
        lf = tk.Frame(topbar, bg=C["topbar"])
        lf.pack(side="left", padx=18)
        tk.Label(lf, text="🔍", font=fnt(17), bg=C["topbar"]).pack(side="left")
        lt = tk.Frame(lf, bg=C["topbar"])
        lt.pack(side="left", padx=(8,0))
        tk.Label(lt, text="Smart Retail Inspector",
                 font=fnt(13,"bold"), bg=C["topbar"], fg=C["text"]).pack(anchor="w")
        tk.Label(lt, text="AI Computer Vision for Business",
                 font=fnt(8), bg=C["topbar"], fg=C["text3"]).pack(anchor="w")

        # Kanan: jam + kasir
        rf = tk.Frame(topbar, bg=C["topbar"])
        rf.pack(side="right", padx=18)
        self.lbl_clock = tk.Label(rf, text="", font=fnt(9),
                                   bg=C["topbar"], fg=C["text2"])
        self.lbl_clock.pack(anchor="e")
        kf = tk.Frame(rf, bg=C["topbar"])
        kf.pack(anchor="e", pady=(4,0))
        tk.Label(kf, text="👤", font=fnt(10), bg=C["topbar"]).pack(side="left")
        self.var_kasir = tk.StringVar(value=self.kasir)
        tk.Entry(kf, textvariable=self.var_kasir, font=fnt(9,"bold"),
                 bg=C["primary_lt"], fg=C["primary"], insertbackground=C["primary"],
                 relief="flat", bd=0, width=14,
                 highlightthickness=1, highlightbackground=C["primary"],
                 highlightcolor=C["primary"]).pack(side="left", padx=(6,0), ipady=4)
        self.var_kasir.trace_add("write",
            lambda *_: setattr(self,"kasir", self.var_kasir.get()))

        # Main
        main = tk.Frame(self, bg=C["bg"])
        main.pack(fill="both", expand=True)
        self._build_left(main)
        self._build_right(main)

    # ── Panel Kiri (Notebook) ─────────────────────────────────────────────────
    def _build_left(self, parent):
        left = tk.Frame(parent, bg=C["bg"])
        left.pack(side="left", fill="both", expand=True, padx=(12,6), pady=10)

        self._nb = ttk.Notebook(left)
        self._nb.pack(fill="both", expand=True)

        self._tab_cam = tk.Frame(self._nb, bg=C["bg"])
        self._tab_cat = tk.Frame(self._nb, bg=C["bg"])

        self._nb.add(self._tab_cam, text="  📷  AI Kamera  ")
        self._nb.add(self._tab_cat, text="  📋  Katalog Produk  ")
        self._nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self._build_camera_tab(self._tab_cam)
        self._build_catalog_tab(self._tab_cat)

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB KAMERA AI  — Layout 2 kolom: kamera kiri | kontrol kanan
    # ══════════════════════════════════════════════════════════════════════════
    def _build_camera_tab(self, parent):
        # ── Row atas: deps + status ──────────────────────────────────────────
        dep_row = tk.Frame(parent, bg=C["bg"])
        dep_row.pack(fill="x", pady=(6, 4), padx=4)
        for lib, ok in [("OpenCV", HAS_CV2), ("YOLO", HAS_YOLO), ("Pillow", HAS_PIL)]:
            Badge(dep_row,
                  text=("✓  " if ok else "✗  ") + lib,
                  color=C["success_lt"] if ok else C["danger_lt"],
                  fg=C["success"] if ok else C["danger"]).pack(side="left", padx=(0, 6))
        self.lbl_status = tk.Label(dep_row, text="⚪  Kamera belum aktif",
                                    font=fnt(9, "bold"), bg=C["bg"], fg=C["text3"])
        self.lbl_status.pack(side="right")

        # ── Body 2 kolom ─────────────────────────────────────────────────────
        body = tk.Frame(parent, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        # ── Kolom KIRI: canvas kamera ─────────────────────────────────────
        cam_col = tk.Frame(body, bg=C["bg"])
        cam_col.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Canvas dengan ukuran tetap proporsional 16:9
        # Kita pakai fixed height agar tidak mengambil seluruh space
        self.cam_canvas = tk.Canvas(cam_col, bg="#1E293B",
                                     bd=0, highlightthickness=2,
                                     highlightbackground=C["border"],
                                     width=480, height=270)
        self.cam_canvas.pack(fill="both", expand=True)
        self.cam_canvas.bind("<Configure>", self._on_cam_resize)
        self._cam_w = 480
        self._cam_h = 270
        self._draw_cam_placeholder()

        # ── Feedback di bawah kamera ──
        self.lbl_feedback = tk.Label(cam_col, text="",
                                      font=fnt(10, "bold"),
                                      bg=C["bg"], fg=C["success"],
                                      anchor="w")
        self.lbl_feedback.pack(fill="x", pady=(6, 0))

        # ── Kolom KANAN: kontrol + info + shortcuts ───────────────────────
        ctrl_col = tk.Frame(body, bg=C["bg"], width=260)
        ctrl_col.pack(side="right", fill="y")
        ctrl_col.pack_propagate(False)

        # ── 1) Tombol Aktifkan / Stop ──
        btn_card = Card(ctrl_col, pady=12, padx=12)
        btn_card.pack(fill="x", pady=(0, 8))

        tk.Label(btn_card, text="🎥  Kontrol Kamera",
                 font=fnt(10, "bold"), bg=C["surface"], fg=C["text"]).pack(anchor="w", pady=(0, 8))

        self.btn_start = tk.Button(
            btn_card, text="▶   Aktifkan Kamera",
            font=fnt(11, "bold"),
            bg=C["primary"], fg="#FFFFFF",
            activebackground=C["primary_dk"], activeforeground="#FFFFFF",
            relief="flat", bd=0, cursor="hand2", pady=10,
            command=self._cv_start)
        self.btn_start.pack(fill="x", pady=(0, 6))

        self.btn_stop = tk.Button(
            btn_card, text="■   Stop Kamera",
            font=fnt(10, "bold"),
            bg=C["danger_lt"], fg=C["danger"],
            activebackground="#FECACA", activeforeground=C["danger"],
            relief="flat", bd=0, cursor="hand2", pady=8,
            state="disabled", command=self._cv_stop)
        self.btn_stop.pack(fill="x")

        if not (HAS_CV2 and HAS_YOLO and HAS_PIL):
            self.btn_start.config(state="disabled")
            tk.Label(btn_card,
                     text="⚠  pip install ultralytics\n    opencv-python pillow",
                     font=fnt(8), bg=C["surface"], fg=C["danger"],
                     justify="left").pack(anchor="w", pady=(6, 0))

        # Sample ID
        sid_row = tk.Frame(btn_card, bg=C["surface"])
        sid_row.pack(fill="x", pady=(8, 0))
        tk.Label(sid_row, text="Sample ID:", font=fnt(8),
                 bg=C["surface"], fg=C["text3"]).pack(side="left")
        self.lbl_sample = tk.Label(sid_row, text=self.sample_id,
                                    font=fnt(9, "bold"),
                                    bg=C["primary_lt"], fg=C["primary"],
                                    padx=6, pady=2)
        self.lbl_sample.pack(side="right")

        # ── 2) Panel Deteksi ──
        det_card = Card(ctrl_col, pady=10, padx=12)
        det_card.pack(fill="x", pady=(0, 8))

        tk.Label(det_card, text="🎯  Deteksi Sekarang",
                 font=fnt(10, "bold"), bg=C["surface"], fg=C["text"]).pack(anchor="w", pady=(0, 6))

        # Nama PRODUK (bukan YOLO class) — paling menonjol
        row1 = tk.Frame(det_card, bg=C["surface"])
        row1.pack(fill="x", pady=2)
        tk.Label(row1, text="Produk:", font=fnt(8),
                 bg=C["surface"], fg=C["text3"], width=8, anchor="w").pack(side="left")
        self.lbl_detect_name = tk.Label(row1, text="Belum ada deteksi",
                                         font=fnt(11, "bold"),
                                         bg=C["surface"], fg=C["primary"],
                                         wraplength=150, justify="left")
        self.lbl_detect_name.pack(side="left", padx=(4, 0))

        # YOLO class + confidence (info teknis kecil)
        row1b = tk.Frame(det_card, bg=C["surface"])
        row1b.pack(fill="x", pady=1)
        tk.Label(row1b, text="", font=fnt(8),
                 bg=C["surface"], fg=C["text3"], width=8, anchor="w").pack(side="left")
        self.lbl_detect_conf = tk.Label(row1b, text="Arahkan produk ke kamera",
                                         font=fnt(8),
                                         bg=C["surface"], fg=C["text3"])
        self.lbl_detect_conf.pack(side="left", padx=(4, 0))

        # SKU
        row2 = tk.Frame(det_card, bg=C["surface"])
        row2.pack(fill="x", pady=2)
        tk.Label(row2, text="SKU:", font=fnt(8),
                 bg=C["surface"], fg=C["text3"], width=8, anchor="w").pack(side="left")
        self.lbl_detect_sku = tk.Label(row2, text="",
                                        font=fnt(8),
                                        bg=C["surface"], fg=C["text2"])
        self.lbl_detect_sku.pack(side="left", padx=(4, 0))

        # Info keranjang (qty × harga = subtotal)
        row3 = tk.Frame(det_card, bg=C["surface"])
        row3.pack(fill="x", pady=2)
        tk.Label(row3, text="Keranjang:", font=fnt(8),
                 bg=C["surface"], fg=C["text3"], width=8, anchor="w").pack(side="left")
        self.lbl_detect_product = tk.Label(row3, text="—",
                                            font=fnt(8, "bold"),
                                            bg=C["surface"], fg=C["text2"],
                                            wraplength=160, justify="left")
        self.lbl_detect_product.pack(side="left", padx=(4, 0))

        # Harga satuan — kotak biru
        row4 = tk.Frame(det_card, bg=C["primary_lt"],
                        highlightthickness=0)
        row4.pack(fill="x", pady=(6, 0))
        tk.Label(row4, text="Harga Satuan", font=fnt(8),
                 bg=C["primary_lt"], fg=C["primary"],
                 padx=8, pady=4).pack(side="left")
        self.lbl_detect_price = tk.Label(row4, text="—",
                                          font=fnt(12, "bold"),
                                          bg=C["primary_lt"], fg=C["primary"],
                                          padx=8, pady=4)
        self.lbl_detect_price.pack(side="right")

        # Brand
        row5 = tk.Frame(det_card, bg=C["surface"])
        row5.pack(fill="x", pady=(4, 0))
        self.lbl_detect_brand = tk.Label(row5, text="",
                                          font=fnt(8),
                                          bg=C["surface"], fg=C["text2"])
        self.lbl_detect_brand.pack(anchor="w", padx=8)

        # E-commerce referensi
        row6 = tk.Frame(det_card, bg=C["surface"])
        row6.pack(fill="x", pady=(2, 4))
        self.lbl_detect_ecom = tk.Label(row6, text="",
                                         font=fnt(8),
                                         bg=C["surface"], fg=C["info"],
                                         wraplength=220, justify="left")
        self.lbl_detect_ecom.pack(anchor="w", padx=8)
        kbd_card = Card(ctrl_col, pady=10, padx=12)
        kbd_card.pack(fill="x", pady=(0, 8))

        tk.Label(kbd_card, text="⌨   Keyboard Shortcuts",
                 font=fnt(10, "bold"), bg=C["surface"], fg=C["text"]).pack(anchor="w", pady=(0, 8))

        shortcuts = [
            ("SPACE", "Tambah ke keranjang",  C["primary"],  C["primary_lt"]),
            ("TAB",   "Ganti deteksi",         C["info"],     C["info_lt"]),
            ("U",     "Undo item terakhir",    C["warning"],  C["warning_lt"]),
            ("C",     "Checkout / bayar",      C["success"],  C["success_lt"]),
            ("N",     "Reset keranjang",       C["text2"],    C["kbd_bg"]),
            ("S",     "Simpan inspeksi CSV",   C["info"],     C["info_lt"]),
            ("Q",     "Keluar",                C["danger"],   C["danger_lt"]),
        ]
        for key, desc, fg_color, bg_color in shortcuts:
            row = tk.Frame(kbd_card, bg=C["surface"])
            row.pack(fill="x", pady=2)
            # Tombol key
            tk.Label(row, text=f" {key} ",
                     font=("Consolas", 9, "bold"),
                     bg=bg_color, fg=fg_color,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=fg_color,
                     padx=6, pady=3, width=6, anchor="center").pack(side="left")
            tk.Label(row, text=f"  {desc}",
                     font=fnt(9), bg=C["surface"],
                     fg=C["text2"]).pack(side="left", padx=(4, 0))

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB KATALOG
    # ══════════════════════════════════════════════════════════════════════════
    def _build_catalog_tab(self, parent):
        self._search_ph = True

        top = tk.Frame(parent, bg=C["bg"])
        top.pack(fill="x", pady=(10,6))

        # Search
        sf = tk.Frame(top, bg=C["surface"],
                      highlightthickness=1, highlightbackground=C["border"])
        sf.pack(side="left", fill="x", expand=True)
        tk.Label(sf, text="🔍", font=fnt(11),
                 bg=C["surface"], fg=C["text3"], padx=8).pack(side="left")
        self.var_search = tk.StringVar()
        self.entry_search = tk.Entry(sf, textvariable=self.var_search,
                                     font=fnt(10), bg=C["surface"], fg=C["text3"],
                                     insertbackground=C["primary"],
                                     relief="flat", bd=0)
        self.entry_search.pack(side="left", fill="x", expand=True, ipady=9, padx=(0,8))
        self.entry_search.insert(0, "Cari produk atau SKU...")
        self.entry_search.bind("<FocusIn>",  self._search_in)
        self.entry_search.bind("<FocusOut>", self._search_out)

        # Filter kategori
        cats = ["Semua"] + sorted({v.get("category","") for v in CATALOG.values() if v.get("category")})
        self.var_cat = tk.StringVar(value="Semua")
        cat_cb = ttk.Combobox(top, textvariable=self.var_cat,
                              values=cats, state="readonly", font=fnt(9), width=16)
        cat_cb.pack(side="left", padx=(8,0), ipady=5)
        cat_cb.bind("<<ComboboxSelected>>", self._on_cat_search)
        self.var_search.trace_add("write", self._on_cat_search)

        self.lbl_count = tk.Label(parent, text="", font=fnt(8),
                                   bg=C["bg"], fg=C["text3"])
        self.lbl_count.pack(anchor="e", padx=4)

        # Tabel
        tw = tk.Frame(parent, bg=C["surface"],
                      highlightthickness=1, highlightbackground=C["border"])
        tw.pack(fill="both", expand=True)
        cols = ("yolo_class","sku","product","brand","category","price")
        self.tree_cat = ttk.Treeview(tw, columns=cols,
                                      show="headings", selectmode="browse")
        conf = {"yolo_class":(90,  "w", "YOLO Class"),
                "sku":        (80,  "w", "SKU"),
                "product":    (210, "w", "Nama Produk"),
                "brand":      (100, "w", "Brand"),
                "category":   (100, "w", "Kategori"),
                "price":      (100, "e", "Harga")}
        for col,(w,anc,hdr) in conf.items():
            self.tree_cat.heading(col, text=hdr,
                                  command=lambda c=col: self._sort(c))
            self.tree_cat.column(col, width=w, anchor=anc, stretch=(col=="product"))
        self.tree_cat.tag_configure("even", background=C["row_even"])
        self.tree_cat.tag_configure("odd",  background=C["row_odd"])
        vsb = ttk.Scrollbar(tw, orient="vertical", command=self.tree_cat.yview)
        self.tree_cat.configure(yscrollcommand=vsb.set)
        self.tree_cat.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Tombol tambah manual
        bar = tk.Frame(parent, bg=C["bg"])
        bar.pack(fill="x", pady=(8,0))
        tk.Label(bar, text="Qty:", font=fnt(10),
                 bg=C["bg"], fg=C["text2"]).pack(side="left")
        self.var_qty = tk.StringVar(value="1")
        tk.Spinbox(bar, from_=1, to=999, textvariable=self.var_qty,
                   font=fnt(10,"bold"), bg=C["surface"], fg=C["primary"],
                   insertbackground=C["primary"], buttonbackground=C["border"],
                   relief="flat", bd=0, width=5,
                   highlightthickness=1, highlightbackground=C["border"]
                   ).pack(side="left", padx=(6,12), ipady=5)
        PrimaryBtn(bar, text="➕  Tambah ke Keranjang",
                   command=self._cat_add_manual).pack(side="left")
        tk.Label(bar, text="atau double-click baris",
                 font=fnt(8), bg=C["bg"], fg=C["text3"]).pack(side="left", padx=(10,0))
        self.tree_cat.bind("<Double-1>", lambda e: self._cat_add_manual())

        self._reload_catalog()

    def _reload_catalog(self):
        self.tree_cat.delete(*self.tree_cat.get_children())
        q   = "" if self._search_ph else self.var_search.get().lower().strip()
        cat = self.var_cat.get() if hasattr(self,"var_cat") else "Semua"
        rows = []
        for cls, item in CATALOG.items():
            if cat != "Semua" and item.get("category","") != cat: continue
            if q and q not in item["product"].lower() and q not in cls.lower() \
               and q not in item.get("sku","").lower(): continue
            rows.append((cls, item))
        for i,(cls,item) in enumerate(rows):
            self.tree_cat.insert("","end", iid=cls,
                                 tags=("even" if i%2==0 else "odd",),
                                 values=(cls,
                                         item.get("sku",""),
                                         item["product"],
                                         item.get("brand","—"),
                                         item.get("category",""),
                                         rupiah(item["price_idr"])))
        if hasattr(self,"lbl_count"):
            self.lbl_count.config(text=f"{len(rows)} produk")

    def _search_in(self, e):
        if self._search_ph:
            e.widget.delete(0,"end"); e.widget.config(fg=C["text"])
            self._search_ph = False

    def _search_out(self, e):
        if not e.widget.get():
            e.widget.insert(0,"Cari produk atau SKU...")
            e.widget.config(fg=C["text3"]); self._search_ph = True

    def _on_cat_search(self, *_):
        self._reload_catalog()

    def _sort(self, col):
        items   = [(self.tree_cat.set(k,col),k) for k in self.tree_cat.get_children("")]
        reverse = self._sort_state.get(col, False)
        try:
            items.sort(key=lambda t: int(t[0].replace("Rp","").replace(".","").strip()),
                       reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for idx,(_,k) in enumerate(items):
            self.tree_cat.move(k,"",idx)
            self.tree_cat.item(k, tags=("even" if idx%2==0 else "odd",))
        self._sort_state[col] = not reverse

    def _cat_add_manual(self):
        sel = self.tree_cat.focus()
        if not sel: return
        item = CATALOG.get(sel)
        if not item: return
        try: qty = max(1, int(self.var_qty.get()))
        except: qty = 1
        self._add_to_cart(sel, item["product"], item["price_idr"],
                          item.get("sku",""), qty, source="MANUAL")

    # ── Panel Kanan (Keranjang) ───────────────────────────────────────────────
    def _build_right(self, parent):
        right = tk.Frame(parent, bg=C["bg"], width=440)
        right.pack(side="right", fill="both", padx=(6,12), pady=10)
        right.pack_propagate(False)

        cart_card = Card(right, padx=0, pady=0)
        cart_card.pack(fill="both", expand=True)

        # Header keranjang
        ch = tk.Frame(cart_card, bg=C["primary"], pady=11, padx=16)
        ch.pack(fill="x")
        tk.Label(ch, text="🛒  Keranjang Belanja",
                 font=fnt(11,"bold"), bg=C["primary"], fg="#FFF").pack(side="left")
        self.lbl_badge = tk.Label(ch, text="kosong",
                                   font=fnt(8), bg=C["primary"], fg="#BFDBFE")
        self.lbl_badge.pack(side="right")

        # Tabel keranjang
        cw = tk.Frame(cart_card, bg=C["surface"])
        cw.pack(fill="both", expand=True)
        ccols = ("nama","qty","harga","subtotal")
        self.tree_cart = ttk.Treeview(cw, columns=ccols,
                                       show="headings", selectmode="browse")
        cconf = {"nama":(175,"w","Produk"),"qty":(45,"center","Qty"),
                 "harga":(95,"e","Harga"),"subtotal":(105,"e","Subtotal")}
        for col,(w,anc,hdr) in cconf.items():
            self.tree_cart.heading(col,text=hdr)
            self.tree_cart.column(col,width=w,anchor=anc,stretch=(col=="nama"))
        self.tree_cart.tag_configure("even",background=C["row_even"])
        self.tree_cart.tag_configure("odd", background=C["row_odd"])
        cvsb = ttk.Scrollbar(cw, orient="vertical", command=self.tree_cart.yview)
        self.tree_cart.configure(yscrollcommand=cvsb.set)
        self.tree_cart.pack(side="left", fill="both", expand=True)
        cvsb.pack(side="right", fill="y")

        # Aksi keranjang
        ab = tk.Frame(cart_card, bg=C["surface"], padx=12, pady=8)
        ab.pack(fill="x")
        SecondaryBtn(ab, text="➖  Kurang 1",
                     command=self._dec_cart).pack(side="left", padx=(0,6))
        DangerBtn(ab, text="🗑  Hapus",
                  command=self._remove_cart).pack(side="left")
        SecondaryBtn(ab, text="↩  Undo [U]",
                     command=self._undo).pack(side="right")

        Divider(cart_card).pack(fill="x")

        # Total panel
        tp = tk.Frame(cart_card, bg=C["surface"], padx=16, pady=12)
        tp.pack(fill="x")
        self.lbl_items = tk.Label(tp, text="", font=fnt(8),
                                   bg=C["surface"], fg=C["text3"])
        self.lbl_items.pack(anchor="e", pady=(0,4))
        tr = tk.Frame(tp, bg=C["surface"])
        tr.pack(fill="x", pady=(0,12))
        tk.Label(tr, text="Total", font=fnt(11),
                 bg=C["surface"], fg=C["text2"]).pack(side="left")
        self.lbl_total = tk.Label(tr, text="Rp 0",
                                   font=fnt(22,"bold"),
                                   bg=C["surface"], fg=C["text"])
        self.lbl_total.pack(side="right")

        # Tombol checkout + shortcut hint
        SuccessBtn(tp, text="💳  CHECKOUT  [C]",
                   command=self._checkout).pack(fill="x")
        SecondaryBtn(tp, text="🔄  Reset Keranjang  [N]",
                     command=self._reset_cart).pack(fill="x", pady=(6,0))

    # ── Keyboard Bindings ─────────────────────────────────────────────────────
    def _bind_keys(self):
        self.bind("<space>",   lambda e: self._key_space())
        self.bind("<Tab>",     lambda e: self._key_tab())
        self.bind("u",         lambda e: self._undo())
        self.bind("U",         lambda e: self._undo())
        self.bind("c",         lambda e: self._checkout())
        self.bind("C",         lambda e: self._checkout())
        self.bind("n",         lambda e: self._reset_cart())
        self.bind("N",         lambda e: self._reset_cart())
        self.bind("s",         lambda e: self._key_save())
        self.bind("S",         lambda e: self._key_save())
        self.bind("q",         lambda e: self._on_close())
        self.bind("Q",         lambda e: self._on_close())
        self.bind("<Escape>",  lambda e: self._on_close())

    def _key_space(self):
        """SPACE: tambah produk terdeteksi ke keranjang (+1 setiap tekan)."""
        if not self._cv_detects:
            self._set_feedback("⚠  Tidak ada objek terdeteksi", color=C["warning"])
            return
        label, conf = self._cv_detects[self._cv_sel % len(self._cv_detects)]
        item = CATALOG.get(label)
        if not item:
            return
        # Tambah 1 unit ke keranjang
        self._add_to_cart(label, item["product"], item["price_idr"],
                          item.get("sku", ""), 1, source="WEBCAM")
        # Feedback jelas: nama produk nyata (bukan YOLO class)
        qty_now = self.cart.get(label, {}).get("qty", 1)
        subtotal = item["price_idr"] * qty_now
        self._set_feedback(
            f"✅  +1  {item['product']}  |  "
            f"Qty: {qty_now}  |  Subtotal: {rupiah(subtotal)}",
            color=C["success"])

    def _key_tab(self):
        """TAB: ganti pilihan deteksi."""
        if not self._cv_detects:
            return
        self._cv_sel = (self._cv_sel + 1) % len(self._cv_detects)
        self._update_detect_labels()
        label, conf = self._cv_detects[self._cv_sel]
        item = CATALOG.get(label, {})
        self._set_feedback(
            f"🔄  Pilih: {label}  →  {item.get('product', '—')}",
            color=C["info"])

    def _key_save(self):
        """S: simpan inspeksi ke CSV dengan gambar ber-bounding box."""
        if not self._cv_detects:
            self._set_feedback("⚠  Tidak ada objek untuk disimpan", color=C["warning"])
            return
        label, conf = self._cv_detects[self._cv_sel % len(self._cv_detects)]
        item = CATALOG.get(label)
        if not item:
            return

        # Ambil qty dari keranjang jika sudah ada, default 1
        qty = self.cart.get(label, {}).get("qty", 1)

        # Gunakan frame yang sudah ada bounding box (annotated)
        with self._cv_lock:
            annotated = self._cv_annotated

        path = save_inspection_csv(
            label, conf, "WEBCAM",
            self.sample_id, qty=qty,
            annotated_frame=annotated   # gambar dengan bbox YOLO
        )
        self._increment_sample()
        subtotal = item["price_idr"] * qty
        self._set_feedback(
            f"💾  Disimpan: {item['product']}  "
            f"qty:{qty}  subtotal:{rupiah(subtotal)}  "
            f"→ {path.name}",
            color=C["warning"])

    # ── Cart logic ────────────────────────────────────────────────────────────
    def _add_to_cart(self, yolo_class, name, price, sku, qty, source=""):
        if yolo_class not in self.cart:
            self.cart[yolo_class] = {"sku": sku, "name": name,
                                      "price": price, "qty": 0}
        self.cart[yolo_class]["qty"] += qty
        self.undo_stack.append((yolo_class, qty))
        self._refresh_cart()

    def _refresh_cart(self):
        self.tree_cart.delete(*self.tree_cart.get_children())
        total = 0; items = 0
        for i, (cls, item) in enumerate(self.cart.items()):
            sub    = item["price"] * item["qty"]
            total += sub; items += item["qty"]
            self.tree_cart.insert("","end", iid=cls,
                                  tags=("even" if i%2==0 else "odd",),
                                  values=(item["name"][:24], item["qty"],
                                          rupiah(item["price"]), rupiah(sub)))
        self.lbl_total.config(text=rupiah(total))
        n = len(self.cart)
        self.lbl_badge.config(text=f"{n} jenis · {items} item" if n else "kosong")
        self.lbl_items.config(
            text=f"{n} jenis  ·  {items} item total" if n else "Keranjang kosong")

    def _dec_cart(self):
        sel = self.tree_cart.focus()
        if not sel or sel not in self.cart: return
        self.cart[sel]["qty"] -= 1
        if self.cart[sel]["qty"] <= 0: del self.cart[sel]
        self._refresh_cart()

    def _remove_cart(self):
        sel = self.tree_cart.focus()
        if sel and sel in self.cart:
            del self.cart[sel]; self._refresh_cart()

    def _undo(self):
        if not self.undo_stack: return
        cls, qty = self.undo_stack.pop()
        if cls in self.cart:
            self.cart[cls]["qty"] -= qty
            if self.cart[cls]["qty"] <= 0: del self.cart[cls]
        self._refresh_cart()
        self._set_feedback("↩  Undo berhasil", color=C["warning"])

    def _reset_cart(self):
        if not self.cart:
            self._set_feedback("Keranjang sudah kosong", color=C["text3"])
            return
        if not messagebox.askyesno("Reset Keranjang",
                "Hapus semua item dari keranjang?", parent=self):
            return
        self.cart.clear()
        self.undo_stack.clear()
        self._refresh_cart()
        self._set_feedback("🔄  Keranjang direset", color=C["info"])

    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Keranjang Kosong",
                "Tambahkan produk terlebih dahulu.\nGunakan SPACE saat kamera aktif,\natau double-click produk di tab Katalog.",
                parent=self); return
        CheckoutDialog(self, dict(self.cart), self.kasir, self._checkout_ok)

    def _checkout_ok(self, invoice, path, kembalian, bayar):
        total = sum(i["price"]*i["qty"] for i in self.cart.values())
        self.cart.clear(); self.undo_stack.clear()
        self._refresh_cart()
        ReceiptDialog(self, invoice, path, kembalian, bayar, total)

    # ── Computer Vision ───────────────────────────────────────────────────────
    def _on_cam_resize(self, event):
        """Pertahankan aspek rasio 16:9 saat canvas di-resize."""
        w = max(event.width, 100)
        h = int(w * 9 / 16)
        # Set height canvas agar proporsional
        self.cam_canvas.config(height=h)
        self._cam_w = w
        self._cam_h = h
        if not self._cv_running:
            self._draw_cam_placeholder()

    def _draw_cam_placeholder(self):
        self.cam_canvas.delete("all")
        self.cam_canvas.update_idletasks()
        w = self.cam_canvas.winfo_width()  or self._cam_w
        h = self.cam_canvas.winfo_height() or self._cam_h
        self.cam_canvas.config(bg="#1E293B")
        # Ikon kamera
        self.cam_canvas.create_text(w//2, h//2 - 32, text="📷",
                                     font=fnt(30), fill="#334155")
        # Teks utama — lebih besar dan jelas
        self.cam_canvas.create_rectangle(w//2-140, h//2-8, w//2+140, h//2+30,
                                          fill="#2563EB", outline="")
        self.cam_canvas.create_text(w//2, h//2+11,
                                     text="▶   Klik Aktifkan Kamera",
                                     font=fnt(12, "bold"), fill="#FFFFFF")
        self.cam_canvas.create_text(w//2, h//2+48,
                                     text="Lalu tekan  SPACE  saat objek terdeteksi",
                                     font=fnt(9), fill="#64748B")

    def _cv_start(self):
        if self._cv_running: return
        if not (HAS_CV2 and HAS_YOLO and HAS_PIL):
            messagebox.showerror("Dependensi Kurang",
                "Install terlebih dahulu:\n\npip install ultralytics opencv-python pillow",
                parent=self); return

        self._set_status("⏳  Memuat model YOLO...", C["warning"])
        self.update()
        try:
            self._cv_model = YOLO(str(MODEL_PATH))
        except Exception as ex:
            messagebox.showerror("Gagal Muat Model", str(ex), parent=self)
            self._set_status("❌  Gagal muat model", C["danger"]); return

        source = self.args.image if self.args.image else None
        if source:
            self._cv_cap = None
            self._cv_static_img = cv2.imread(str(source))
            if self._cv_static_img is None:
                messagebox.showerror("Gambar Tidak Ditemukan",
                    f"File tidak bisa dibaca:\n{source}", parent=self); return
        else:
            self._cv_cap = cv2.VideoCapture(self.args.camera,
                cv2.CAP_DSHOW if __import__("os").name == "nt" else cv2.CAP_ANY)
            if not self._cv_cap.isOpened():
                messagebox.showerror("Kamera Tidak Ditemukan",
                    "Tidak bisa membuka webcam.\n"
                    "Periksa izin kamera di Settings → Privacy → Camera.\n"
                    "Atau coba: python app.py --camera 1",
                    parent=self)
                self._cv_cap = None; return

        self._cv_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self._set_status("🟢  Kamera aktif", C["success"])
        self._cv_thread = threading.Thread(target=self._cv_loop, daemon=True)
        self._cv_thread.start()
        self._cv_update_canvas()

    def _cv_stop(self):
        self._cv_running = False
        if self._cv_cap:
            self._cv_cap.release(); self._cv_cap = None
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self._set_status("⚫  Kamera dimatikan", C["text3"])
        self._cv_detects = []; self._cv_sel = 0
        self._update_detect_labels()
        self._draw_cam_placeholder()

    def _cv_loop(self):
        """Thread background: baca frame, jalankan YOLO."""
        while self._cv_running:
            if self._cv_cap is not None:
                ok, frame = self._cv_cap.read()
                if not ok: break
            else:
                frame = self._cv_static_img.copy()
                time.sleep(0.05)

            try:
                result    = self._cv_model.predict(
                    frame, conf=self.args.conf, imgsz=640, verbose=False)[0]
                annotated = result.plot()   # BGR frame dengan bounding box
            except Exception:
                annotated = frame; result = None

            # Kumpulkan deteksi yang ada di catalog DAN tidak di blacklist
            detects = {}
            if result is not None:
                for b in result.boxes:
                    name = result.names[int(b.cls.item())]
                    conf = float(b.conf.item())
                    # Abaikan: person, kendaraan, hewan, furnitur, dll
                    if name in YOLO_BLACKLIST:
                        continue
                    if name in CATALOG and conf > detects.get(name, ("", 0))[1]:
                        detects[name] = (name, conf)
            sorted_det = sorted(detects.values(), key=lambda x: -x[1])

            with self._cv_lock:
                self._cv_frame     = frame.copy()       # raw — untuk referensi
                self._cv_annotated = annotated.copy()   # sudah ada bbox YOLO
                self._cv_detects   = sorted_det
                if self._cv_sel >= max(1, len(sorted_det)):
                    self._cv_sel = 0
                # Convert annotated → PIL untuk canvas Tkinter
                rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                self._cv_pil = Image.fromarray(rgb)
        self._cv_running = False

    def _cv_update_canvas(self):
        """Polling 33ms: render frame ke canvas dengan overlay info deteksi."""
        if not self._cv_running:
            return

        with self._cv_lock:
            pil_img = self._cv_pil
            detects = list(self._cv_detects)
            sel_idx = self._cv_sel

        if pil_img:
            try:
                # Pakai ukuran canvas aktual agar frame pas dan tidak blur
                self.cam_canvas.update_idletasks()
                w = self.cam_canvas.winfo_width()
                h = self.cam_canvas.winfo_height()
                if w < 10 or h < 10:
                    w, h = self._cam_w, self._cam_h

                resized = pil_img.resize((w, h), Image.LANCZOS)
                draw    = ImageDraw.Draw(resized, "RGBA")

                if detects:
                    label, conf = detects[sel_idx % len(detects)]
                    item = CATALOG[label]
                    # Overlay bar bawah
                    bar_h = 60
                    draw.rectangle([0, h - bar_h, w, h],
                                   fill=(15, 23, 42, 210))
                    # Garis aksen biru kiri
                    draw.rectangle([0, h - bar_h, 5, h],
                                   fill=(37, 99, 235, 255))
                    # Baris 1: NAMA PRODUK (yang penting) + confidence
                    product_name = item["product"]
                    txt1 = f"  {product_name}   conf:{conf:.2f}  (YOLO:{label})"
                    draw.text((8, h - bar_h + 7), txt1, fill=(255, 255, 255))
                    # Baris 2: harga + instruksi
                    txt2 = (f"  Harga: {rupiah(item['price_idr'])}  "
                            f"·  SPACE = +1 ke keranjang  "
                            f"·  S = simpan inspeksi")
                    draw.text((8, h - bar_h + 34), txt2, fill=(167, 243, 208))
                    # Indikator multi-deteksi
                    if len(detects) > 1:
                        draw.text((w - 110, h - bar_h + 20),
                                   f"TAB {sel_idx+1}/{len(detects)}",
                                   fill=(148, 163, 184))
                else:
                    draw.rectangle([0, h - 38, w, h], fill=(15, 23, 42, 170))
                    draw.text((12, h - 25),
                               "  Arahkan produk ke kamera...",
                               fill=(148, 163, 184))

                self._cv_tk_img = ImageTk.PhotoImage(resized)
                self.cam_canvas.delete("all")
                self.cam_canvas.create_image(0, 0, anchor="nw",
                                              image=self._cv_tk_img)
                self.after(0, self._update_detect_labels)

            except Exception:
                pass

        self.after(33, self._cv_update_canvas)

    def _update_detect_labels(self):
        if self._cv_detects:
            label, conf = self._cv_detects[self._cv_sel % len(self._cv_detects)]
            item        = CATALOG.get(label, {})
            qty_in_cart = self.cart.get(label, {}).get("qty", 0)
            subtotal    = item.get("price_idr", 0) * qty_in_cart

            # Warna confidence: hijau >= 0.70 | kuning >= 0.50 | merah < 0.50
            if conf >= 0.70:
                conf_color = C["success"]
                conf_icon  = "✓"
            elif conf >= 0.50:
                conf_color = C["warning"]
                conf_icon  = "~"
            else:
                conf_color = C["danger"]
                conf_icon  = "⚠"

            # Nama produk nyata (bukan kelas YOLO generik)
            self.lbl_detect_name.config(
                text=item.get("product", label), fg=C["primary"])

            # Confidence + kelas YOLO (info teknis)
            self.lbl_detect_conf.config(
                text=f"{conf_icon}  conf: {conf:.2f}  |  YOLO class: {label}",
                fg=conf_color)

            # SKU
            self.lbl_detect_sku.config(text=item.get("sku", ""))

            # Harga satuan
            self.lbl_detect_price.config(
                text=rupiah(item.get("price_idr", 0)))

            # Baris produk: tampilkan brand + kategori, atau qty di keranjang
            brand    = item.get("brand", "")
            category = item.get("category", "")
            ecom     = item.get("ecommerce_ref", "")
            if qty_in_cart > 0:
                self.lbl_detect_product.config(
                    text=f"✅  Di keranjang: {qty_in_cart} × "
                         f"{rupiah(item.get('price_idr', 0))} "
                         f"= {rupiah(subtotal)}",
                    fg=C["success"])
            else:
                info = f"🏷  {brand}  ·  {category}" if brand else category
                self.lbl_detect_product.config(text=info, fg=C["text2"])

            # Update label brand dan e-commerce jika widget ada
            if hasattr(self, "lbl_detect_brand"):
                self.lbl_detect_brand.config(
                    text=f"🏷  {brand}" if brand else "")
            if hasattr(self, "lbl_detect_ecom"):
                self.lbl_detect_ecom.config(
                    text=f"🛒  {ecom}" if ecom else "")
        else:
            self.lbl_detect_name.config(
                text="Belum ada produk terdeteksi", fg=C["text3"])
            self.lbl_detect_conf.config(
                text="Arahkan produk ke kamera", fg=C["text3"])
            self.lbl_detect_sku.config(text="")
            self.lbl_detect_product.config(text="—", fg=C["text3"])
            self.lbl_detect_price.config(text="—")
            if hasattr(self, "lbl_detect_brand"):
                self.lbl_detect_brand.config(text="")
            if hasattr(self, "lbl_detect_ecom"):
                self.lbl_detect_ecom.config(text="")

    def _increment_sample(self):
        self._sample_no += 1
        self.sample_id = f"ITEM-{self._sample_no:03d}"
        self.lbl_sample.config(text=self.sample_id)

    # ── Utility ───────────────────────────────────────────────────────────────
    def _set_status(self, text, color=None):
        self.lbl_status.config(text=text, fg=color or C["text2"])

    def _set_feedback(self, text, color=None):
        self.lbl_feedback.config(text=text, fg=color or C["success"])
        self.after(3000, lambda: self.lbl_feedback.config(text=""))

    def _tick(self):
        self.lbl_clock.config(
            text=datetime.now().strftime("%A, %d %B %Y   %H:%M:%S"))
        self.after(1000, self._tick)

    def _on_tab_change(self, event):
        if "Katalog" in event.widget.tab("current","text") and self._cv_running:
            self._cv_stop()

    def _on_close(self):
        self._cv_running = False
        if self._cv_cap: self._cv_cap.release()
        self.destroy()


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Smart Retail Inspector — AI Vision for Business",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python app.py                    # webcam default
  python app.py --camera 1         # webcam ke-2
  python app.py --image foto.jpg   # mode gambar statis
  python app.py --conf 0.30        # turunkan threshold deteksi

Keyboard Shortcuts:
  SPACE  Tambah produk terdeteksi ke keranjang
  TAB    Ganti pilihan deteksi
  U      Undo item terakhir
  C      Checkout / bayar
  N      New / reset keranjang
  S      Simpan inspeksi ke CSV
  Q/Esc  Keluar
        """)
    parser.add_argument("--camera", type=int, default=0,
                        help="Index webcam (default: 0)")
    parser.add_argument("--image",  type=str, default=None,
                        help="Path gambar statis sebagai pengganti webcam")
    parser.add_argument("--conf",   type=float, default=0.40,
                        help="Threshold confidence YOLO 0-1 (default: 0.40)")
    args = parser.parse_args()

    app = RetailInspectorApp(args)
    app.protocol("WM_DELETE_WINDOW", app._on_close)
    app.mainloop()


if __name__ == "__main__":
    main()
