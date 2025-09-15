#!/usr/bin/env python3
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

def generate_key_pair() -> tuple[bytes, bytes]:
    """
    Generate a public/private key pair for digital signatures.
    
    Returns:
        Tuple of (private_key_pem, public_key_pem)
    
    Method: AI assistance + cryptography library documentation
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

def sign_message(message: str, private_key_pem: bytes) -> str:
    """
    Sign a message using a private key.
    
    Args:
        message: The message to sign
        private_key_pem: The private key in PEM format
    
    Returns:
        Base64 encoded signature
    
    Method: AI assistance + cryptography library documentation
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
    )
    
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(message: str, signature: str, public_key_pem: bytes) -> bool:
    """
    Verify a digital signature.
    
    Args:
        message: The original message
        signature: Base64 encoded signature
        public_key_pem: The public key in PEM format
    
    Returns:
        True if signature is valid, False otherwise
    
    Method: AI assistance + cryptography library documentation
    """
    try:
        public_key = serialization.load_pem_public_key(public_key_pem)
        signature_bytes = base64.b64decode(signature.encode('utf-8'))
        
        public_key.verify(
            signature_bytes,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False