
class fuzzy_rule:
    def __init__(self, rule_id, antecedent, consequent):
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent

    def hitung_firing_strength(self, membership):
        nilai = []

        for variabel, label in self.antecedent.items():
            nilai.append(membership[variabel][label])

        return min(nilai)

    def tampilkan(self, membership):
        alpha = self.hitung_firing_strength(membership)

        print(
            f"{self.rule_id}: "
            f"{self.antecedent} -> {self.consequent}, "
            f"alpha = {alpha:.2f}"
        )


# basis aturan produksi roti
rule_base = [
    fuzzy_rule("R1", {"permintaan": "rendah", "stok": "sedikit"}, "berkurang"),
    fuzzy_rule("R2", {"permintaan": "rendah", "stok": "sedang"}, "berkurang"),
    fuzzy_rule("R3", {"permintaan": "rendah", "stok": "banyak"}, "berkurang"),
    fuzzy_rule("R4", {"permintaan": "sedang", "stok": "sedikit"}, "bertambah"),
    fuzzy_rule("R5", {"permintaan": "sedang", "stok": "sedang"}, "tetap"),
    fuzzy_rule("R6", {"permintaan": "sedang", "stok": "banyak"}, "berkurang"),
    fuzzy_rule("R7", {"permintaan": "tinggi", "stok": "sedikit"}, "bertambah"),
    fuzzy_rule("R8", {"permintaan": "tinggi", "stok": "sedang"}, "bertambah"),
    fuzzy_rule("R9", {"permintaan": "tinggi", "stok": "banyak"}, "tetap")
]


# data hasil fuzzifikasi
membership = {
    "permintaan": {
        "rendah": 0.2,
        "sedang": 0.8,
        "tinggi": 0.0
    },
    "stok": {
        "sedikit": 0.0,
        "sedang": 0.5,
        "banyak": 0.5
    }
}


# pengujian seluruh aturan
print("HASIL PENGUJIAN BASIS ATURAN PRODUKSI ROTI")
print("-" * 50)

for rule in rule_base:
    rule.tampilkan(membership)

print("\nATURAN YANG AKTIF:")

for rule in rule_base:
    alpha = rule.hitung_firing_strength(membership)

    if alpha > 0:
        print(
            f"{rule.rule_id} -> Produksi {rule.consequent}, "
            f"alpha = {alpha:.2f}"
        )
