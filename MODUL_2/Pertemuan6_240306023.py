
# praktikum 6 - fuzzy rule dan knowledge base

class fuzzy_rule:
    def __init__(self, rule_id, antecedent, consequent, operator="AND"):
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        nilai_derajat = []

        for var_nama, label_nama in self.antecedent.items():
            derajat = derajat_fuzzifikasi[var_nama].get(label_nama, 0.0)
            nilai_derajat.append(derajat)

        if not nilai_derajat:
            return 0.0

        if self.operator == "AND":
            return min(nilai_derajat)
        elif self.operator == "OR":
            return max(nilai_derajat)
        else:
            raise ValueError("Operator tidak dikenali")

    def __str__(self):
        syarat = f" {self.operator} ".join(
            [f"{var} is {label}"
             for var, label in self.antecedent.items()]
        )
        hasil = ", ".join(
            [f"{var} is {label}"
             for var, label in self.consequent.items()]
        )
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"


# basis aturan kipas pendingin server
rule_base = [
    fuzzy_rule("R1", {"suhu": "Dingin", "cpu": "Ringan"},
               {"kipas": "Lambat"}),
    fuzzy_rule("R2", {"suhu": "Dingin", "cpu": "Sedang"},
               {"kipas": "Sedang"}),
    fuzzy_rule("R3", {"suhu": "Dingin", "cpu": "Berat"},
               {"kipas": "Cepat"}),
    fuzzy_rule("R4", {"suhu": "Normal", "cpu": "Ringan"},
               {"kipas": "Lambat"}),
    fuzzy_rule("R5", {"suhu": "Normal", "cpu": "Sedang"},
               {"kipas": "Sedang"}),
    fuzzy_rule("R6", {"suhu": "Normal", "cpu": "Berat"},
               {"kipas": "Cepat"}),
    fuzzy_rule("R7", {"suhu": "Panas", "cpu": "Ringan"},
               {"kipas": "Sedang"}),
    fuzzy_rule("R8", {"suhu": "Panas", "cpu": "Sedang"},
               {"kipas": "Cepat"}),
    fuzzy_rule("R9", {"suhu": "Panas", "cpu": "Berat"},
               {"kipas": "Cepat"}),
]


# data input sesuai modul
derajat_input = {
    "suhu": {
        "Dingin": 0.2,
        "Normal": 0.8,
        "Panas": 0.0
    },
    "cpu": {
        "Ringan": 0.0,
        "Sedang": 0.5,
        "Berat": 0.5
    }
}


# evaluasi semua aturan
print("=" * 60)
print("HASIL EVALUASI BASIS ATURAN FUZZY")
print("=" * 60)

aturan_aktif = []

for rule in rule_base:
    alpha = rule.hitung_firing_strength(derajat_input)
    kipas = rule.consequent["kipas"]

    if alpha > 0:
        status = f"AKTIF (alpha = {alpha:.2f})"
        aturan_aktif.append((rule.rule_id, kipas, alpha))
    else:
        status = "NONAKTIF"

    print(f"{rule} --> {status}")


print("\n" + "=" * 60)
print("RINGKASAN ATURAN AKTIF")
print("=" * 60)

for rule_id, kipas, alpha in aturan_aktif:
    print(f"{rule_id}: Kipas = {kipas}, alpha = {alpha:.2f}")

print(f"\nTotal aturan aktif: {len(aturan_aktif)} dari {len(rule_base)}")
