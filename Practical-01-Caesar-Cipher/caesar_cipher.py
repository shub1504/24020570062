"""Practical 1: Caesar cipher (substitution cipher)."""

def caesar_cipher(text: str, shift: int) -> str:
    """Shift alphabetic characters; preserve case and punctuation."""
    result = []
    shift %= 26
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(char)
    return "".join(result)


def main():
    message = input("Enter message: ")
    shift = int(input("Enter shift value (e.g. 3): "))
    encrypted = caesar_cipher(message, shift)
    decrypted = caesar_cipher(encrypted, -shift)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)


if __name__ == "__main__":
    main()
