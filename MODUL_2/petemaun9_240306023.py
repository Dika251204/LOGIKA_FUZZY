"""Praktikum 9 - Metode Sugeno (TSK Orde 0 dan 1) dan Tsukamoto, komparasi dengan Mamdani
Nama : Dika Rizki Ananda   NIM : 240306023
Berkas tugas (Bagian F). Fungsi inti sama dengan kode pembanding modul (Bagian D:
pertemuan9_sugeno_tsukamoto.py). Bagian program:
  1. Fungsi inti Sugeno (rata-rata terbobot) dan Tsukamoto (fungsi invers monoton)
  2. Studi kasus data jurnal: produksi roti Cinderela Bread House (Sahulata dkk., 2020)
  3. Tugas Praktikum 9: alokasi bandwidth dinamis (Sugeno Orde 0 vs Tsukamoto, 5 variasi input)
Pustaka: numpy saja."""
import numpy as np
 
# ==========================================================
# 1. FUNGSI INTI (sama dengan kode modul)
# ==========================================================
def hitung_sugeno(alphas, z_values):
    """Rata-rata terbobot: z* = sum(alpha_i * z_i) / sum(alpha_i)."""
    alphas = np.array(alphas, dtype=float)
    z_values = np.array(z_values, dtype=float)
    total = np.sum(alphas)
    return 0.0 if total == 0 else float(np.sum(alphas * z_values) / total)
 
 
def invers_monoton_naik(alpha, a, b):
    """Kurva naik (0 di a, 1 di b): z = a + alpha*(b-a)."""
    return a + alpha * (b - a)
 
 
def invers_monoton_turun(alpha, a, b):
    """Kurva turun (1 di a, 0 di b): z = b - alpha*(b-a)."""
    return b - alpha * (b - a)
 
 
def hitung_tsukamoto(alphas, fungsi_invers_list):
    z_values = [f(a) for a, f in zip(alphas, fungsi_invers_list)]
    return hitung_sugeno(alphas, z_values), z_values
 
 
# Fungsi keanggotaan skalar
def mf_turun(x, a, b):          # bahu kiri: 1 sampai a, turun ke 0 di b
    return float(min(1.0, max(0.0, (b - x) / (b - a))))
 
def mf_naik(x, a, b):           # bahu kanan: 0 sampai a, naik ke 1 di b
    return float(min(1.0, max(0.0, (x - a) / (b - a))))
 
def mf_segitiga(x, a, b, c):
    return float(max(0.0, min((x - a) / (b - a), (c - x) / (c - b))))
 
 
# ==========================================================
# 2. STUDI KASUS DATA JURNAL: PRODUKSI ROTI CINDERELA
# ==========================================================
def mu_demand(x):
    return {"Sedikit": mf_turun(x, 120, 142), "Sedang": mf_segitiga(x, 120, 142, 164),
            "Banyak": mf_naik(x, 142, 164)}
 
def mu_stock(y):
    return {"Sedikit": mf_turun(y, 69, 79), "Sedang": mf_segitiga(y, 69, 79, 88),
            "Banyak": mf_naik(y, 79, 88)}
 
RULES = [("Sedikit", "Sedikit", "Sedikit"), ("Sedikit", "Sedang", "Sedikit"),
         ("Sedikit", "Banyak", "Sedikit"), ("Sedang", "Sedikit", "Banyak"),
         ("Sedang", "Sedang", "Sedang"), ("Sedang", "Banyak", "Sedang"),
         ("Banyak", "Sedikit", "Banyak"), ("Banyak", "Sedang", "Banyak"),
         ("Banyak", "Banyak", "Banyak")]
 
# Himpunan output produksi pada grid 1001 titik
Z = np.linspace(190, 260, 1001)
MF_OUT = {"Sedikit": np.interp(Z, [190, 214, 237, 260], [1, 1, 0, 0]),
          "Sedang":  np.interp(Z, [190, 214, 237, 259, 260], [0, 0, 1, 0, 0]),
          "Banyak":  np.interp(Z, [190, 237, 259, 260], [0, 0, 1, 1])}
 
# Konstanta Sugeno Orde 0 = centroid analitik tiap himpunan output (dihitung eksak dari bentuk
# kurva: Sedikit = bahu + sisi turun, Sedang = segitiga, Banyak = sisi naik + bahu)
C = {"Sedikit": 208.368, "Sedang": 236.667, "Banyak": 252.323}
 
# Pusat himpunan input untuk Sugeno Orde 1: z = p*x + q*y + r,  r = c - p*x_c - q*y_c
XC = {"Sedikit": 120.0, "Sedang": 142.0, "Banyak": 164.0}
YC = {"Sedikit": 69.0, "Sedang": 79.0, "Banyak": 88.0}
P, Q = 0.5, -0.3
 
# Fungsi invers Tsukamoto. Catatan: himpunan 'Sedang' berbentuk segitiga, sehingga
# hanya cabang naik yang dipakai sebagai kriteria monotonik lokal (batasan metode).
INV = {"Sedikit": lambda a: invers_monoton_turun(a, 214, 237),
       "Sedang":  lambda a: invers_monoton_naik(a, 214, 237),
       "Banyak":  lambda a: invers_monoton_naik(a, 237, 259)}
 
 
def firing_strengths(x, y):
    md, ms = mu_demand(x), mu_stock(y)
    return [min(md[d], ms[s]) for d, s, _ in RULES]
 
 
def mamdani(x, y):
    """Max-Min + centroid (verifikasi terhadap hasil MATLAB jurnal)."""
    agr = np.zeros_like(Z)
    for a, (_, _, p) in zip(firing_strengths(x, y), RULES):
        agr = np.fmax(agr, np.fmin(a, MF_OUT[p]))
    return float(np.sum(Z * agr) / np.sum(agr))
 
 
def sugeno0(x, y):
    return hitung_sugeno(firing_strengths(x, y), [C[p] for _, _, p in RULES])
 
 
def sugeno1(x, y):
    zs = [C[p] + P * (x - XC[d]) + Q * (y - YC[s]) for d, s, p in RULES]
    return hitung_sugeno(firing_strengths(x, y), zs)
 
 
def tsukamoto(x, y):
    al = firing_strengths(x, y)
    return hitung_tsukamoto(al, [INV[p] for _, _, p in RULES])[0]
 
 
# (tanggal, permintaan, persediaan, produksi aktual, produksi Mamdani-MATLAB jurnal)
DATA = [("02-06-18", 141, 71, 234, 242), ("04-06-18", 122, 66, 214, 211),
        ("30-08-18", 126, 68, 211, 216), ("31-08-18", 161, 61, 248, 252)]
 
 
def studi_kasus_roti():
    print("=" * 70)
    print("2. STUDI KASUS ROTI CINDERELA")
    print("   Konstanta Sugeno-0 (centroid):", {k: round(v, 3) for k, v in C.items()})
    hdr = ["Tanggal", "Perm", "Pers", "Aktual", "Mamdani", "Sug-0", "Sug-1", "Tsuk", "Mam(centroid)"]
    print(" | ".join(f"{h:>9}" for h in hdr))
    sel = {"s0": [], "s1": [], "ts": []}
    gal = {"mam": [], "s0": [], "s1": [], "ts": []}
    for tgl, x, y, akt, mam in DATA:
        s0, s1, ts, mc = sugeno0(x, y), sugeno1(x, y), tsukamoto(x, y), mamdani(x, y)
        print(" | ".join(f"{v:>9}" for v in
              [tgl, x, y, akt, mam, f"{s0:.2f}", f"{s1:.2f}", f"{ts:.2f}", f"{mc:.2f}"]))
        for k, v in (("s0", s0), ("s1", s1), ("ts", ts)):
            sel[k].append(v - mam)
            gal[k].append(abs(v - akt))
        gal["mam"].append(abs(mam - akt))
    print("   Selisih terhadap Mamdani (metode - Mamdani):")
    for tgl, a, b, c in zip([d[0] for d in DATA], sel["s0"], sel["s1"], sel["ts"]):
        print(f"     {tgl}: Sug-0 {a:+.2f} | Sug-1 {b:+.2f} | Tsuk {c:+.2f}")
    print("   Rata-rata |selisih| thd Mamdani:",
          {k: round(float(np.mean(np.abs(v))), 2) for k, v in sel.items()})
    print("   Rata-rata |galat| thd produksi aktual:",
          {k: round(float(np.mean(v)), 2) for k, v in gal.items()})
 
 
# ==========================================================
# 3. TUGAS PRAKTIKUM 9 (BAGIAN F): ALOKASI BANDWIDTH DINAMIS
#    Input : Pengguna Aktif (0-100), Trafik (0-100); Output: Bandwidth 10-100 Mbps
#    Aturan (4): Sedikit/Rendah -> Kecil ; selain itu -> Besar
# ==========================================================
def mu_pengguna(x):
    return {"Sedikit": mf_turun(x, 20, 80), "Banyak": mf_naik(x, 20, 80)}
 
def mu_trafik(t):
    return {"Rendah": mf_turun(t, 20, 80), "Tinggi": mf_naik(t, 20, 80)}
 
RULES_BW = [("Sedikit", "Rendah", "Kecil"), ("Sedikit", "Tinggi", "Besar"),
            ("Banyak", "Rendah", "Besar"), ("Banyak", "Tinggi", "Besar")]
K_BW = {"Kecil": 20.0, "Besar": 85.0}                       # konstanta Sugeno Orde 0 (Mbps)
INV_BW = {"Kecil": lambda a: invers_monoton_turun(a, 10, 60),   # turun: 1 di 10, 0 di 60
          "Besar": lambda a: invers_monoton_naik(a, 40, 100)}   # naik : 0 di 40, 1 di 100
 
 
def bandwidth(u, t):
    mu, mt = mu_pengguna(u), mu_trafik(t)
    al = [min(mu[a], mt[b]) for a, b, _ in RULES_BW]
    s0 = hitung_sugeno(al, [K_BW[c] for _, _, c in RULES_BW])
    ts, zt = hitung_tsukamoto(al, [INV_BW[c] for _, _, c in RULES_BW])
    return al, s0, ts, zt
 
 
def tugas_bandwidth():
    print("=" * 70)
    print("3. TUGAS: ALOKASI BANDWIDTH (Mbps)")
    uji = [(10, 15), (30, 70), (50, 50), (75, 25), (95, 90)]
    print(" | ".join(f"{h:>10}" for h in ["Pengguna", "Trafik", "Sugeno-0", "Tsukamoto", "Selisih"]))
    for u, t in uji:
        al, s0, ts, zt = bandwidth(u, t)
        print(" | ".join(f"{v:>10}" for v in [u, t, f"{s0:.2f}", f"{ts:.2f}", f"{ts - s0:+.2f}"]))
        print(f"     alpha R1-R4 = {[round(a, 3) for a in al]}; z Tsukamoto = {[round(z, 2) for z in zt]}")
 
 
if __name__ == "__main__":
    studi_kasus_roti()
    tugas_bandwidth()
