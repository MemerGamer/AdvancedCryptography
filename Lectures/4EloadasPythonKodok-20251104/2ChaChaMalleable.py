import os
from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305

class ChaCha20Cipher:
    def __init__(self, key, nonce=None):
        self.key = key
        if nonce is None:
            self.nonce = os.urandom(12)
        else:
            self.nonce = nonce

    def encrypt(self, plaintext):
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, self.nonce

    def decrypt(self, ciphertext, nonce):
        cipher = ChaCha20.new(key=self.key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def encryptPoly1305(self, plaintext):
        cipher = ChaCha20_Poly1305.new(key=self.key, nonce=self.nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext, tag, self.nonce,

    def decryptPoly1305(self, ciphertext, tag, nonce):
        cipher = ChaCha20_Poly1305.new(key=self.key, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext

def demonstrate_chacha20_bit_flipping():
    print("\n=== ChaCha20 Bit Flipping tamadas ===")

    key = os.urandom(32)
    cipher = ChaCha20Cipher(key)

    message = b"FROM:12345|TO:67890|AMOUNT:0100.00|CURRENCY:USD"
    initM   = b"0100.00"
    targetM = b"9900.00"
    ciphertext, nonce = cipher.encrypt(message)
    original_decrypted = cipher.decrypt(ciphertext, nonce)
    print(f"Original: {original_decrypted.decode()}")
    print(f"Ciphertext: {ciphertext.hex()}")

    # tamadas: kicsereljuk "initM"-t "targetM-re, ahol a hossz egyforma
    modified_ciphertext = bytearray(ciphertext)
    approve_pos = message.find(initM)

    for i, (orig, target) in enumerate(zip(initM, targetM)):
        diff = orig ^ target
        # modofied_c = orig ^ key ^ orig ^ target
        modified_ciphertext[approve_pos + i] ^= diff
    print(f"Modified ciphertext (hex): {bytes(modified_ciphertext).hex()}")
    # visszafejtjuk a modositott ciphertext-et
    # result = key ^ modofied_c = key ^ orig ^ key ^ orig ^ target = target
    result = cipher.decrypt(bytes(modified_ciphertext), nonce)
    print(f"After bit flipping: {result.decode()}")
    print(f"✓ ChaCha20 is also malleable - message changed from {initM} to {targetM}!")

def demonstrate_chacha20_with_nonce_reuse():
    print("\n=== ChaCha20 ujrafelhasznalt nonce ===")

    # a kulcs es nonce generálása
    key = os.urandom(32)
    nonce = os.urandom(12)

    # ket kulonbozo message ugyanazzal a kukccsal valo titkositasa, XOR-olása
    message1 = b"Transfer $100 to account 12345"
    message2 = b"Transfer $956 to account 12345"
    cipher1 = ChaCha20Cipher(key, nonce)
    cipher2 = ChaCha20Cipher(key, nonce)
    ciphertext1, _ = cipher1.encrypt(message1)
    ciphertext2, _ = cipher2.encrypt(message2)
    print(f"Message 1: {message1.decode()}")
    print(f"Message 2: {message2.decode()}")
    print(f"Same nonce used for both encryptions!")

    # Tamadas: XOR-oljuk a ket ciphertext-et
    xor_ciphertexts = bytes([c1 ^ c2 for c1, c2 in zip(ciphertext1, ciphertext2)])
    print(f"\nXOR of ciphertexts: {xor_ciphertexts.hex()}")

    # ha ismert az egyik message akkor meg lehet hatarozni a masik message-t
    print("\nIf attacker knows one plaintext, they can recover the other:")
    recovered_message2 = bytes([m1 ^ x for m1, x in zip(message1, xor_ciphertexts)])
    print(f"Recovered message 2: {recovered_message2.decode()}")

    print("✓ Nonce reuse allows complete message recovery!")

def demonstrate_protection_with_aead():
    print("\n=== Protection with ChaCha20-Poly1305 (AEAD) ===")

    key = os.urandom(32)
    cipher = ChaCha20Cipher(key)

    message = b"FROM:12345|TO:67890|AMOUNT:0100.00|CURRENCY:USD"
    initM = b"0100.00"
    targetM = b"9900.00"
    ciphertext, tag, nonce = cipher.encryptPoly1305(message)
    original_decrypted = cipher.decryptPoly1305(ciphertext, tag, nonce)
    print(f"Original: {original_decrypted.decode()}")
    print(f"Ciphertext: {ciphertext.hex()}")

    # tamadas: kicsereljuk "initM"-t "targetM-re, ahol a hossz egyforma
    modified_ciphertext = bytearray(ciphertext)
    approve_pos = message.find(initM)

    for i, (orig, target) in enumerate(zip(initM, targetM)):
        diff = orig ^ target
        modified_ciphertext[approve_pos + i] ^= diff
    print(f"Modified ciphertext: {bytes(modified_ciphertext).hex()}")
    # megprobaljuk visszafejteni a modositott ciphertext-et
    try:
        result = cipher.decryptPoly1305(bytes(modified_ciphertext), tag, nonce)
    except Exception as e:
        print(f"✓ Decryption failed: {e}")
        print("✓ Authentication protected against modification!")

demonstrate_chacha20_bit_flipping()
demonstrate_chacha20_with_nonce_reuse()
demonstrate_protection_with_aead()
