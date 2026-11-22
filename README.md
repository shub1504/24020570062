# Data Privacy Practicals (Python)

A student-friendly repository containing 13 practicals covering classical ciphers, hashing, password security, digital signatures, privacy audits, impact assessment, regulatory compliance, anonymization and data ethics.

## Requirements
- Python 3.10+
- Install dependencies: `python -m pip install -r requirements.txt`
- Most programs use the Python standard library. Practical 4 uses `requests`; Practical 7 uses `cryptography`; Practical 11 uses `requests` and `beautifulsoup4`.

## Run
Scripts work from the repository root or from inside their own folder, for example:
```bash
python Practical-01-Caesar-Cipher/caesar_cipher.py
```

## Practical index
1. Caesar cipher — substitution cipher demonstration.
2. Rail Fence cipher — transposition cipher demonstration.
3. SHA-256 — one-way password hashing demonstration (not suitable for storing real passwords by itself).
4. Password breach checker — Have I Been Pwned Pwned Passwords range API using k-anonymity.
5. Passphrase generator — cryptographically secure random word selection.
6. Brute-force simulation — deliberately small local-only demonstration.
7. Digital signature — RSA-PSS signing and verification of a document.
8. Privacy audit — sample organizational audit and checklist.
9. Compliance plan — India DPDP Act, 2023 and DPDP Rules, 2025 readiness plan.
10. Data ethics — ethical considerations and risk assessment.
11. Website privacy audit — passive Python audit script plus manual privacy-policy review.
12. Privacy Impact Assessment — PIA of a typical ride-hailing platform (location data, DPDP Act 2023).
13. Anonymization — identifier removal, masking, generalisation, k-anonymity, l-diversity and differential privacy on synthetic data.

## Safety and privacy notes
- Do not put real passwords, personal data, API keys, private keys or confidential documents in this repository.
- Practical 4 uses a dummy sample file. Never commit a real credential list.
- Practical 6 is a toy demonstration. Only test passwords you own and keep the search space tiny.
- Practical 13 uses only fictional, synthetic records.
- Practical 11 must only be run on sites you own or have permission to test.
- Practical 7 generates a fresh private key locally. Keep `private_key.pem` secret; do not upload it to GitHub. The script writes keys into a local `keys/` folder and `.gitignore` excludes it.
- SHA-256 alone is not a password-storage scheme. Real applications should use Argon2id, scrypt, bcrypt or PBKDF2 with a unique salt and suitable work factor.
- This is an educational project, not a legal compliance certification or legal advice.

## GitHub upload
Create an empty GitHub repository named `Data-Privacy-Practicals`, then run:
```bash
git init
git add .
git commit -m "Add data privacy practicals 1-13"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Data-Privacy-Practicals.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Do not publish secret keys or real credentials.

## Suggested viva preparation
For every practical, be ready to explain: objective, input, algorithm, important functions, output, limitations and one real-world use case.
