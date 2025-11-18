import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def aesECB_Security():
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_ECB)
    print('Az egyforma blokkok egyforma rejtjelezett szovegblokkot eredmenyeznek:\n')

    plaintext = b'SAPI2025ELTE2024SAPI2025ELTE2024'
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    print(f'a nyiltszoveg blokkjai: {[plaintext[i : i + 16] for i in range(0, len(plaintext), 16)]}')
    print(f'a rejtjelezett szoveg blokkjai: {[ciphertext[i: i + 16].hex() for i in range(0, len(ciphertext), 16)]}')
    print('\n')

    print('A nyiltszoveg mintazata megjelenik a rejtjelezett szovegben:')
    patternData =  []
    for i in range(8):
        if i % 2 == 0:
            patternData.extend([b'SAPI2025ELTE2024'] * 4)
        else:
            patternData.extend([b'MUSZAKI_BUDAPEST'] * 4)
    patternData =  b''.join(patternData)
    cipherPatternData = cipher.encrypt(pad(patternData, AES.block_size))

    print(f'a nyiltszoveg blokkjai:  {[patternData[i:i + 16].hex() for i in range(0, len(patternData), 16)]}')
    print(f'a rejtjelezett szoveg blokkjai: {[cipherPatternData[i:i + 16].hex() for i in range(0, len(cipherPatternData), 16)]}')

    print('\nAz ECB-t nem szabad hasznalni!')

aesECB_Security()

