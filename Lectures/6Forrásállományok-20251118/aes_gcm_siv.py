from Crypto.Cipher import AES
import os

keySize = 32
key = os.urandom(keySize)
nonce = os.urandom(keySize//2)
aad = b'https://www.ms.sapientia.ro/~mgyongyi/'
message = b'EMTE-Sapientia, Matematika-Informatika Tanszek'
cipher = AES.new(key, AES.MODE_SIV, nonce)
cipher.update(aad)
ciphertext, tag = cipher.encrypt_and_digest(message)
print(ciphertext.hex())
print(tag.hex())

aad = b'https://www.ms.sapientia.ro/~mgyongyi/'
try:
    cipher = AES.new(key, AES.MODE_SIV, nonce)
    cipher.update(aad)
    message = cipher.decrypt_and_verify(ciphertext, tag)
    print('visszafejtett uzenet: ', message.decode())
except:
    print('visszafejtesi hiba!')