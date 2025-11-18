import random, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BS = AES.block_size

def encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(plaintext, BS))
    return iv + ciphertext

def decrypt(key, ciphertext):
    iv = ciphertext[:BS]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ciphertext[BS:]), BS)

def securityGame(m0, m1, iv, key, countSuccess):
    b = random.randint(0, 1)
    chosen = m0 if b == 0 else m1
    c = encrypt(key, chosen, iv)
    print("Rejtjelezett szoveg:", c.hex())
    guess = int(input('valassz: 0 vagy 1: '))
    print("Talalat:", guess == b)
    return countSuccess + (guess == b)

# m = b"az osztalyzat elegtelen"
# print(BS)
# iv = os.urandom(BS)
# key = os.urandom(16)
# c = encrypt(key, m, iv)
# print("Rejtjelezett szoveg:", c.hex())
# p = decrypt(key, c)
# print('Visszafejtett szoveg: ', p.decode())

m0 = b"    az osztalyzat jeles"
m1 = b"az osztalyzat elegtelen"
iv = os.urandom(BS)
key = os.urandom(16)
countSuccess = 0
for i in range(10):
    countSuccess = securityGame(m0, m1, iv, key, countSuccess)
print(f'helyes talalatszam: {countSuccess}\n\n')

key = os.urandom(16)
countSuccess = 0
for i in range(10):
    iv = os.urandom(BS)
    countSuccess = securityGame(m0, m1, iv, key, countSuccess)
print(f'helyes talalatszam: {countSuccess}')