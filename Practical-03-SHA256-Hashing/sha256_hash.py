"""Practical 3: SHA-256 hexadecimal digest."""

import hashlib


def sha256_hex(password: str) -> str:
    """Return the SHA-256 digest of a UTF-8 string as hexadecimal."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    value = input("Enter a sample string to hash: ")
    print("SHA-256:", sha256_hex(value))
    print("\nNote: SHA-256 is one-way hashing, not encryption.")
    print("Do not store production passwords as plain SHA-256 hashes.")
