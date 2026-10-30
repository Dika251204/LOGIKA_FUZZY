
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# 1. Semesta kualitas sinyal
z = np.linspace(0, 100, 1000)

# 2. Fungsi keanggotaan
mf_jelek = fuzz.trapmf(z, [0, 0, 25, 45])
mf_sedang = fuzz.trimf(z, [35, 55, 75])
mf_bagus = fuzz.trapmf(z, [65, 85, 100, 100])

# 3. Nilai firing rules
alpha_jelek = 0.5
alpha_sedang = 0.8
alpha_bagus = 0.2

# 4. Implikasi MIN dan agregasi MAX
agregasi = np.fmax(
    np.fmin(alpha_jelek, mf_jelek),
    np.fmax(
        np.fmin(alpha_sedang, mf_sedang),
        np.fmin(alpha_bagus, mf_bagus)
    )
)

# 5. Menghitung lima metode defuzzifikasi
metode = ["centroid", "bisector", "mom", "som", "lom"]
hasil = {}

for m in metode:
    hasil[m.upper()] = fuzz.defuzz(z, agregasi, m)

# 6. Menampilkan hasil di terminal
print("\nHASIL DEFUZZIFIKASI KUALITAS WIFI")
print("-" * 38)
print(f"{'Metode':<12} | {'Nilai':>10}")
print("-" * 38)

for nama, nilai in hasil.items():
    print(f"{nama:<12} | {nilai:>10.3f}")

# 7. Membuat grafik seperti gambar referensi
plt.figure(figsize=(12, 7))

# Kurva agregasi dan area di bawah kurva
plt.plot(
    z, agregasi,
    color="blue",
    linewidth=2.5,
    label="Kurva Agregasi Fuzzy"
)

plt.fill_between(
    z, agregasi, 0,
    color="skyblue",
    alpha=0.4
)

# Warna masing-masing metode
warna = {
    "CENTROID": "red",
    "BISECTOR": "purple",
    "MOM": "black",
    "SOM": "green",
    "LOM": "orange"
}

# Garis vertikal dan titik penanda
for nama, nilai in hasil.items():
    plt.axvline(
        x=nilai,
        color=warna[nama],
        linestyle="--",
        linewidth=2,
        label=f"{nama} ({nilai:.2f})"
    )

    # Titik pada kurva di posisi hasil defuzzifikasi
    tinggi = np.interp(nilai, z, agregasi)

    plt.scatter(
        nilai, tinggi,
        color=warna[nama],
        s=70,
        zorder=5
    )

# Judul dan keterangan sumbu
plt.title(
    "Perbandingan 5 Metode Defuzzifikasi WiFi",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Kualitas Sinyal (skala 0–100)", fontsize=12)
plt.ylabel("Derajat Keanggotaan μ(z)", fontsize=12)

plt.xlim(0, 100)
plt.ylim(0, 1.05)

plt.grid(True, linestyle=":", alpha=0.7)
plt.legend(loc="upper right")
plt.tight_layout()

# Simpan grafik
plt.savefig("wifi_defuzzifikasi.png", dpi=300)

# Tampilkan grafik
plt.show()
