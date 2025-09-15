#!/usr/bin/env python3
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def hash_password(password: str, salt: bytes = None) -> tuple[str, bytes]:
    """
    Hash a password using PBKDF2 with SHA-256.
    
    Args:
        password: The password to hash
        salt: Optional salt (if None, generates a random one)
    
    Returns:
        Tuple of (hashed_password_hex, salt)
    
    Method: AI assistance + Internet research for PBKDF2 best practices
    """
    if salt is None:
        salt = secrets.token_bytes(32)
    
    # Use PBKDF2 with SHA-256 for secure password hashing
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # High iteration count for security
    )
    
    key = kdf.derive(password.encode('utf-8'))
    return key.hex(), salt

def verify_password(password: str, hashed_password: str, salt: bytes) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: The password to verify
        hashed_password: The stored hash (hex string)
        salt: The salt used for hashing
    
    Returns:
        True if password matches, False otherwise
    """
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, hashed_password)