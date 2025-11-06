import random, os
from Crypto.Cipher import AES

BS = AES.block_size

def encrypt(key, plaintext, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext)
    return nonce + ciphertext

def decrypt(key, ciphertext):
    nonce = ciphertext[:BS // 2]
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(ciphertext[BS // 2:])

def securityGame(m0, m1, nonce, key, countSuccess):
    b = random.randint(0, 1)
    chosen = m0 if b == 0 else m1
    c = encrypt(key, chosen, nonce)
    print("Rejtjelezett szoveg:", c.hex())
    guess = int(input('valassz: 0 vagy 1: '))
    print("Talalat:", guess == b)
    return countSuccess + (guess == b)

m0 = b"    az osztalyzat jeles"
m1 = b"az osztalyzat elegtelen"
nonce = os.urandom(BS // 2)
key = os.urandom(16)
countSuccess = 0
for i in range(10):
    countSuccess = securityGame(m0, m1, nonce, key, countSuccess)
print(f'helyes talalatszam: {countSuccess}\n\n')

key = os.urandom(16)
countSuccess = 0
for i in range(10):
    nonce = os.urandom(BS // 2)
    countSuccess = securityGame(m0, m1, nonce, key, countSuccess)
print(f'helyes talalatszam: {countSuccess}')