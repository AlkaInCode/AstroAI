"""
Symmetric encryption for storing user-supplied LLM API keys at rest.

A user's key is decrypted only in-memory, server-side, at the moment of
making their LLM call -- it is never returned to the frontend after saving,
never logged. Deriving a Fernet key from an arbitrary passphrase (via
SHA-256) lets ENCRYPTION_KEY be configured the same way as this app's other
secrets (e.g. JWT_SECRET_KEY): any string, with a dev default that must be
overridden in production.
"""

import base64
import hashlib

from cryptography.fernet import Fernet

from app.config import settings


def _fernet() -> Fernet:
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.encryption_key.encode()).digest())
    return Fernet(key)


def encrypt_secret(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_secret(ciphertext: str) -> str:
    return _fernet().decrypt(ciphertext.encode()).decode()
