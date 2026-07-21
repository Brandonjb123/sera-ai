# encryption.py
import os
from cryptography.fernet import Fernet

# Ambil kunci enkripsi dari environment, atau generate baru (hanya untuk dev)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"[WARNING] ENCRYPTION_KEY tidak ditemukan. Generated: {ENCRYPTION_KEY}")
    print("[WARNING] Simpan kunci ini di environment variable untuk production!")

fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def encrypt_api_key(api_key: str) -> str:
    """Enkripsi API key sebelum disimpan ke database."""
    if not api_key:
        return ""
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    """Dekripsi API key yang diambil dari database."""
    if not encrypted_key:
        return ""
    return fernet.decrypt(encrypted_key.encode()).decode()