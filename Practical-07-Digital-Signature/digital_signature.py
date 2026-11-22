"""Practical 7: Sign a document and verify its digital signature with RSA-PSS."""

from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

BASE = Path(__file__).resolve().parent
KEY_DIR = BASE / "keys"
KEY_DIR.mkdir(exist_ok=True)
PRIVATE_PATH = KEY_DIR / "private_key.pem"
PUBLIC_PATH = KEY_DIR / "public_key.pem"
DOCUMENT_PATH = BASE / "signed_document.txt"
SIGNATURE_PATH = BASE / "document.sig"


def create_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    PRIVATE_PATH.write_bytes(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    PUBLIC_PATH.write_bytes(private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ))
    return private_key


def sign_document():
    private_key = serialization.load_pem_private_key(PRIVATE_PATH.read_bytes(), password=None)
    data = DOCUMENT_PATH.read_bytes()
    signature = private_key.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    SIGNATURE_PATH.write_bytes(signature)
    print("Document signed. Signature saved to:", SIGNATURE_PATH)


def verify_document():
    public_key = serialization.load_pem_public_key(PUBLIC_PATH.read_bytes())
    try:
        public_key.verify(
            SIGNATURE_PATH.read_bytes(),
            DOCUMENT_PATH.read_bytes(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        print("VALID: signature matches this document.")
    except Exception:
        print("INVALID: document changed or signature/key does not match.")


if __name__ == "__main__":
    import sys
    if not PRIVATE_PATH.exists() or not PUBLIC_PATH.exists():
        create_keys()
        print("A new RSA key pair was generated locally.")
    if not DOCUMENT_PATH.exists():
        DOCUMENT_PATH.write_text(
            "This is a sample document for the digital signature practical.\n",
            encoding="utf-8",
        )
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_document()          # verify only, never re-signs
    else:
        sign_document()
        verify_document()
        print("Tamper demo: edit signed_document.txt, then run: python digital_signature.py verify")
