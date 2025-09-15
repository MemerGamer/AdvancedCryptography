#!/usr/bin/env python3
from cryptography.fernet import Fernet
import base64

def generate_symmetric_key() -> bytes:
    """
    Generate a secure symmetric key for encryption.
    
    Returns:
        A 32-byte symmetric key
    
    Method: AI assistance + cryptography library documentation
    """
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> str:
    """
    Encrypt a message using symmetric encryption.
    
    Args:
        message: The message to encrypt
        key: The symmetric key
    
    Returns:
        Base64 encoded encrypted message
    
    Method: AI assistance + cryptography library documentation
    """
    f = Fernet(key)
    encrypted_token = f.encrypt(message.encode('utf-8'))
    return encrypted_token.decode('utf-8')


def decrypt_message(encrypted_message: str, key: bytes) -> str:
    """
    Decrypt a message using symmetric encryption.
    
    Args:
        encrypted_message: Base64 encoded encrypted message
        key: The symmetric key
    
    Returns:
        The decrypted message
    
    Method: AI assistance + cryptography library documentation
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode('utf-8'))
    return decrypted_message.decode('utf-8')
