# Practical 13: Data Anonymization Techniques

## Aim
To learn data anonymization techniques (identifier removal, masking, generalisation, k-anonymity, l-diversity and differential privacy) and apply them to a small synthetic dataset so that individuals cannot easily be re-identified.

## Files
| File | Purpose |
|---|---|
| `anonymize.py` | Runs all steps and prints the result of each |
| `patients_sample.csv` | 15 **fictional** patient records (never use real data) |
| `anonymized_output.csv` | Released dataset, created when the script runs |

## Run
```bash
python anonymize.py
```
Uses only the Python standard library.

## Key terms
| Term | Meaning |
|---|---|
| Direct identifier | Identifies a person alone (name, phone, email). Remove or pseudonymise it |
| Quasi-identifier | Harmless alone but identifying in combination (age, pincode, gender) |
| Sensitive attribute | The private fact being protected (medical condition) |
| Pseudonymisation | Replace an identifier with a token. Re-linkable by whoever holds the salt, so **not** full anonymisation |
| Generalisation | Make values less precise (age 23 -> 20-29, pincode 110001 -> 110***) |
| Suppression | Remove records that are too unique |
| k-anonymity | Every record looks the same as at least k-1 others on the quasi-identifiers |
| l-diversity | Every group has at least l different sensitive values |
| Differential privacy | Add calibrated random noise so one person's presence barely changes the result |

## Dry-run (what the script does)
1. **Prepare:** `Aarav, 23, 110001` becomes `token 1874f3a1, 20-29, 110***`. The name is gone and the age and pincode are generalised.
2. **Group** the records by (age group, pincode prefix, gender). Group sizes are 2, 3, 3, 2, 3, 1, 1, so the smallest group is 1 and **k = 1**. A group of 1 means that person is unique and can be re-identified.
3. **Suppress** the two single-record groups (50-59 / 110*** / M and 60-69 / 560*** / M). Now the smallest group is 2, so **k = 2**.
4. **Check l-diversity.** The group 50-59 / 110*** / F contains Neha, Tara and Ira, and all three have *Cancer*. Even though the data is 2-anonymous, an attacker who knows a woman aged 50-59 from that area is in the data learns her diagnosis. This is the **homogeneity attack**. Removing non-diverse groups leaves 10 records with **k = 2 and l = 2**.
5. **Differential privacy.** The true count of Cancer patients is 4. With Laplace noise (scale = 1/epsilon): a small epsilon (0.1) gives a very noisy answer (about 14), while epsilon 1 or 5 stays close to 4. Smaller epsilon means more privacy and less accuracy.

## Limitations
- k-anonymity does not stop the homogeneity attack, which is why l-diversity is needed. Neither stops an attacker who has extra outside knowledge.
- Generalisation and suppression reduce data usefulness.
- This demo uses Python's `random` module with a fixed seed so results repeat. Real differential privacy uses a secure noise source and tracks a total privacy budget.
- A pseudonymised token is still personal data under the DPDP Act and GDPR.

## Viva questions
- Anonymisation vs pseudonymisation? Anonymisation is irreversible; pseudonymisation can be reversed with extra information.
- Why remove the name but still risk re-identification? Quasi-identifiers combined (age + pincode + gender) can single out a person.
- What is k-anonymity and what is its weakness? Hidden in a crowd of at least k; fails when the crowd shares the same sensitive value (homogeneity attack).
- What does epsilon control in differential privacy? The privacy/accuracy trade-off.
- Real-world use? Census data releases, and Apple/Google collecting usage statistics.
