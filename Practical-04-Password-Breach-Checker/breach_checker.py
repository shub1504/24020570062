"""Practical 4: Check passwords with HIBP Pwned Passwords range API.

The API receives only the first 5 hex characters of the SHA-1 digest.
The raw password and full hash are never sent to the service.
Input file format: username,password (one pair per line).
Use only dummy/test credentials in the sample file.
"""

import hashlib
import time
from pathlib import Path

import requests

API_URL = "https://api.pwnedpasswords.com/range/"


def breach_count(password: str) -> int:
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    response = requests.get(
        API_URL + prefix,
        headers={"Add-Padding": "true", "User-Agent": "Student-Privacy-Practical"},
        timeout=15,
    )
    response.raise_for_status()
    for line in response.text.splitlines():
        candidate, count = line.split(":")
        if candidate.upper() == suffix:
            return int(count)
    return 0


def check_file(filename: str) -> None:
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",", maxsplit=1)
            if len(parts) != 2:
                print(f"Line {line_number}: skipped (expected username,password)")
                continue
            username, password = (part.strip() for part in parts)
            if not username or not password:
                print(f"Line {line_number}: skipped (empty field)")
                continue
            try:
                count = breach_count(password)
                status = f"FOUND in {count:,} breach records" if count else "not found"
                print(f"{username}: {status}")
                time.sleep(1)  # be considerate to the public API
            except requests.RequestException as error:
                print(f"{username}: API/network error: {error}")


if __name__ == "__main__":
    check_file(Path(__file__).resolve().parent / "passwords.txt")
