import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def dictionaryAttack():
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_ECB)

    # chosen-plaintext attack
    knownBlocks = {}

    # a mini szotar felepitese
    test_strings = [b'USER = admin_____', b'USER = root______', b'ROLE = admin_____',
                    b'PASSWORD = valami', b'MUSZAKI_BUDAPEST', b'SAPIENTIAEGYETEM']

    # a szotar elemek titkositasa
    for test_str in test_strings:
        block = pad(test_str, AES.block_size)
        ciphertext = cipher.encrypt(block)
        knownBlocks[ciphertext[:16]] = test_str
        print(f'Ismert lekepezes: {test_str} -> {ciphertext[:16].hex()}')

    # egy ismeretlennek tekintendo szoveg titkositott ertekenek a meghatarozasa
    secretMessage = b'ROLE = user_____MUSZAKI_BUDAPEST'
    secretCiphertext = cipher.encrypt(pad(secretMessage, AES.block_size))

    print(f'\nA rejtjelezett szoveg, amit az ismert lekepezesek alapjan fel szeretnek torni:\n'
          f'{secretCiphertext.hex()}')

    # a dictinary tamadas inditasa
    print(f'\na dictinary tamadas eredmenye: ')
    recovered = b''
    for i in range(0, len(secretCiphertext), 16):
        block = secretCiphertext[i:i + 16]
        if block in knownBlocks:
            recovered += knownBlocks[block]
            print(f'Block {i // 16}: {knownBlocks[block]} ✅')
        else:
            recovered += b'[UNKNOWN]'
            print(f'Blokk {i // 16}: [UNKNOWN] ❌')

    print(f'\nVisszafejtett szovegresz: {recovered}')

dictionaryAttack()