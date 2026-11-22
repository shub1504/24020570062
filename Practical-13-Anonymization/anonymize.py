"""Practical 13: Data anonymization techniques on a small SYNTHETIC dataset.

Techniques demonstrated (standard library only):
  1. Removing direct identifiers and pseudonymisation (salted hash)
  2. Data masking (phone / email)
  3. Generalisation (age -> range, pincode -> prefix)
  4. k-anonymity check + suppression of small groups
  5. l-diversity check (shows the homogeneity attack)
  6. Differential privacy (Laplace noise on a count)

All names in patients_sample.csv are fictional. Never use real personal data.
"""

import csv
import hashlib
import random
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_FILE = BASE / "patients_sample.csv"
OUTPUT_FILE = BASE / "anonymized_output.csv"

# Quasi-identifiers: harmless alone, but can identify a person when combined.
QUASI_IDENTIFIERS = ("age_group", "pin_prefix", "gender")
SENSITIVE = "condition"


# ---------------------------------------------------------------- 1. identifiers
def pseudonymise(value: str, salt: str) -> str:
    """Replace an identifier by a salted-hash token (pseudonymisation).

    Pseudonymised data can still be re-linked by whoever holds the salt, so
    under privacy law it is NOT fully anonymous.
    """
    return hashlib.sha256((salt + value).encode("utf-8")).hexdigest()[:8]


# ---------------------------------------------------------------- 2. masking
def mask_phone(phone: str) -> str:
    """9876543210 -> 98******10"""
    return phone[:2] + "*" * (len(phone) - 4) + phone[-2:]


def mask_email(email: str) -> str:
    """aarav@example.com -> a****@example.com"""
    user, domain = email.split("@", 1)
    return user[0] + "*" * (len(user) - 1) + "@" + domain


# ---------------------------------------------------------------- 3. generalisation
def generalise_age(age: int) -> str:
    low = (age // 10) * 10
    return f"{low}-{low + 9}"


def generalise_pincode(pincode: str) -> str:
    return pincode[:3] + "***"


# ---------------------------------------------------------------- 4/5. k and l
def group_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[q] for q in QUASI_IDENTIFIERS)].append(row)
    return groups


def k_anonymity(rows) -> int:
    """k = size of the smallest group of rows sharing the same quasi-identifiers."""
    return min(len(g) for g in group_rows(rows).values())


def l_diversity(rows) -> int:
    """l = smallest number of DISTINCT sensitive values inside any group."""
    return min(len({r[SENSITIVE] for r in g}) for g in group_rows(rows).values())


def suppress_small_groups(rows, k: int):
    """Drop every row whose group has fewer than k members."""
    groups = group_rows(rows)
    kept = [r for g in groups.values() if len(g) >= k for r in g]
    return kept, len(rows) - len(kept)


# ---------------------------------------------------------------- 6. differential privacy
def laplace_noise(scale: float, rng: random.Random) -> float:
    """Laplace(0, scale) = difference of two exponential random variables."""
    return rng.expovariate(1 / scale) - rng.expovariate(1 / scale)


def dp_count(true_count: int, epsilon: float, rng: random.Random) -> float:
    """Noisy count. A count changes by at most 1 when one person is added or
    removed (sensitivity = 1), so the noise scale is 1 / epsilon."""
    return true_count + laplace_noise(1 / epsilon, rng)


# ---------------------------------------------------------------- demo
def load_rows():
    with INPUT_FILE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    rows = load_rows()
    salt = "demo-salt-change-me"   # in real life: secret, random, stored separately
    print(f"Loaded {len(rows)} synthetic records.\n")

    print("STEP 1-3: remove identifiers, pseudonymise, generalise")
    prepared = []
    for r in rows:
        prepared.append({
            "token": pseudonymise(r["name"], salt),     # name removed -> token
            "age_group": generalise_age(int(r["age"])),
            "pin_prefix": generalise_pincode(r["pincode"]),
            "gender": r["gender"],
            "condition": r["condition"],
        })
    print("  Original :", rows[0]["name"], rows[0]["age"], rows[0]["pincode"])
    p = prepared[0]
    print("  Released :", p["token"], p["age_group"], p["pin_prefix"], "\n")

    print("STEP 2: masking examples")
    print("  mask_phone('9876543210')        ->", mask_phone("9876543210"))
    print("  mask_email('aarav@example.com') ->", mask_email("aarav@example.com"), "\n")

    print("STEP 4: k-anonymity")
    sizes = {" | ".join(k): len(v) for k, v in group_rows(prepared).items()}
    for key, size in sizes.items():
        print(f"  group [{key}] -> {size} record(s)")
    print("  k BEFORE suppression =", k_anonymity(prepared))
    target_k = 2
    safe, removed = suppress_small_groups(prepared, target_k)
    print(f"  Suppressed {removed} record(s) in groups smaller than {target_k}")
    print("  k AFTER  suppression =", k_anonymity(safe), "\n")

    print("STEP 5: l-diversity (homogeneity attack check)")
    for key, group in group_rows(safe).items():
        values = sorted({r[SENSITIVE] for r in group})
        flag = "  <-- ALL SAME: attacker learns the diagnosis!" if len(values) == 1 else ""
        print(f"  group [{' | '.join(key)}] -> {values}{flag}")
    print("  l =", l_diversity(safe), "(k-anonymous but NOT 2-diverse)\n")

    # Fix: also suppress groups with a single sensitive value.
    diverse = [r for g in group_rows(safe).values()
               if len({x[SENSITIVE] for x in g}) >= 2 for r in g]
    print(f"  After removing non-diverse groups: {len(diverse)} records, "
          f"k = {k_anonymity(diverse)}, l = {l_diversity(diverse)}\n")

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(diverse[0].keys()))
        writer.writeheader()
        writer.writerows(diverse)
    print("  Released dataset saved to:", OUTPUT_FILE.name, "\n")

    print("STEP 6: differential privacy (count of 'Cancer' patients)")
    true_count = Counter(r[SENSITIVE] for r in rows)["Cancer"]
    rng = random.Random(42)       # fixed seed ONLY so the demo is repeatable
    print("  True count =", true_count)
    for eps in (0.1, 1.0, 5.0):
        noisy = dp_count(true_count, eps, rng)
        print(f"  epsilon={eps:<4} -> noisy count = {noisy:.2f}")
    print("  Smaller epsilon = more noise = more privacy, less accuracy.")
    print("  (Real systems use a secure random source and track a privacy budget.)")


if __name__ == "__main__":
    main()
