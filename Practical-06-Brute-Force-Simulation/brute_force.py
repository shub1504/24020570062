"""Practical 6: Tiny, local-only brute-force demonstration.

This deliberately limits the alphabet and maximum length. It does not
connect to accounts, websites, networks or real authentication systems.
"""

from itertools import product
from string import ascii_lowercase, digits


def simulate(target: str, alphabet: str = ascii_lowercase + digits,
             max_length: int = 4) -> tuple[str | None, int]:
    if len(target) > max_length:
        raise ValueError("Target exceeds the configured demo length.")
    if any(char not in alphabet for char in target):
        raise ValueError("Target contains characters outside the demo alphabet.")

    attempts = 0
    for length in range(1, max_length + 1):
        for candidate_tuple in product(alphabet, repeat=length):
            candidate = "".join(candidate_tuple)
            attempts += 1
            if candidate == target:
                return candidate, attempts
    return None, attempts


if __name__ == "__main__":
    # Use a toy password that you choose locally, e.g. "cat".
    target = input("Enter a toy lowercase/digit password (max 4 chars): ")
    try:
        found, attempts = simulate(target)
        print("Matched:", found)
        print("Attempts:", attempts)
    except ValueError as error:
        print("Input error:", error)
    print("This is a classroom simulation, not a tool for attacking accounts.")
