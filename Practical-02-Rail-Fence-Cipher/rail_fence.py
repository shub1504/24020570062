"""Practical 2: Rail Fence transposition cipher."""

def encrypt(message: str, rails: int) -> str:
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")
    fence = [""] * rails
    rail, direction = 0, 1
    for char in message:
        fence[rail] += char
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return "".join(fence)


def decrypt(ciphertext: str, rails: int) -> str:
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")
    # First determine which rail position each character occupied.
    pattern = []
    rail, direction = 0, 1
    for _ in ciphertext:
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    counts = [pattern.count(r) for r in range(rails)]
    rail_chunks, pos = [], 0
    for count in counts:
        rail_chunks.append(list(ciphertext[pos:pos + count]))
        pos += count

    indexes = [0] * rails
    output = []
    for r in pattern:
        output.append(rail_chunks[r][indexes[r]])
        indexes[r] += 1
    return "".join(output)


def main():
    message = input("Enter message: ")
    rails = int(input("Enter number of rails (minimum 2): "))
    cipher = encrypt(message, rails)
    print("Encrypted:", cipher)
    print("Decrypted:", decrypt(cipher, rails))


if __name__ == "__main__":
    main()
