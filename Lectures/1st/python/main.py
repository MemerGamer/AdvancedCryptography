#!/usr/bin/env python3
"""
Main demonstration script for Advanced Cryptography Exercises
"""

import os
import sys
from pathlib import Path

# Add the current directory to the Python path so we can import from exercises
sys.path.insert(0, str(Path(__file__).parent))

from exercises import (
    hash_password, verify_password,
    generate_symmetric_key, encrypt_message, decrypt_message,
    generate_key_pair, sign_message, verify_signature,
    safe_file_access
)

def main():
    """Demonstrate the implemented functions."""
    print("=== Advanced Cryptography Exercises Demo ===\n")
    
    # Exercise 1: Password Hashing
    print("1. Password Hashing:")
    password = "my_secure_password_123"
    hashed_hex, salt = hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed_hex}")
    print(f"Salt: {salt.hex()}")
    print(f"Verification: {verify_password(password, hashed_hex, salt)}")
    print()
    
    # Exercise 2: Symmetric Encryption
    print("2. Symmetric Encryption:")
    message = "This is a secret message!"
    key = generate_symmetric_key()
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    print(f"Original message: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()
    
    # Exercise 3: Digital Signature
    print("3. Digital Signature:")
    message = "This message needs to be signed"
    private_key_pem, public_key_pem = generate_key_pair()
    signature = sign_message(message, private_key_pem)
    is_valid = verify_signature(message, signature, public_key_pem)
    print(f"Message: {message}")
    print(f"Signature: {signature[:50]}...")
    print(f"Signature valid: {is_valid}")
    print()
    
    # Exercise 4: Safe File Access
    print("4. Safe File Access:")
    try:
        # Create test directory and file for demonstration
        os.makedirs("/safedir", exist_ok=True)
        with open("/safedir/test.txt", "w") as f:
            f.write("This is a test file in the safe directory.")
        
        safe_path = safe_file_access("/safedir/test.txt")
        print(f"Safe file access successful: {safe_path}")
        
        # Test with unsafe path
        try:
            unsafe_path = safe_file_access("/etc/passwd")
            print(f"This should not print: {unsafe_path}")
        except ValueError as e:
            print(f"Unsafe access correctly blocked: {e}")
            
    except (ValueError, FileNotFoundError, PermissionError) as e:
        print(f"Safe file access result: {e}")
    print()

if __name__ == "__main__":
    main()