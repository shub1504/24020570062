"""Practical 5: Generate a memorable passphrase using secure randomness."""

import secrets
from pathlib import Path


def generate_passphrase(word_file: str, number_of_words: int = 5) -> str:
    if number_of_words < 4:
        raise ValueError("Choose at least 4 words for this demonstration.")
    words = [
        word.strip().lower()
        for word in Path(word_file).read_text(encoding="utf-8").splitlines()
        if word.strip() and not word.startswith("#")
    ]
    if len(words) < 20:
        raise ValueError("Dictionary file should contain at least 20 words.")
    selected = [secrets.choice(words) for _ in range(number_of_words)]
    return "-".join(selected)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "words.txt"
    print("Generated passphrase:", generate_passphrase(path))
    print("Store it in a password manager; do not reuse it.")
