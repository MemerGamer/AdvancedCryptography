import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = os.urandom(16)
IV = os.urandom(16)  # Initialization vector

ecb_cipher = AES.new(key, AES.MODE_ECB)
cbc_cipher = AES.new(key, AES.MODE_CBC, IV)

plaintext = b'MUSZAKI_BUDAPEST' * 4  # Repeated content

# ECB titkositas
ecb_result = ecb_cipher.encrypt(pad(plaintext, AES.block_size))
# CBC titkositas
cbc_result = cbc_cipher.encrypt(pad(plaintext, AES.block_size))

print(f'Nyilt szoveg: {plaintext}')
print(f'\nECB rejtjelezett szoveg (hex):\n{ecb_result.hex()}')
print(f'CBC rejtjelezett szoveg (hex):\n{cbc_result.hex()}')

# a rejtjelezett blokkok
ecb_blocks = [ecb_result[i:i + 16].hex() for i in range(0, len(ecb_result), 16)]
cbc_blocks = [cbc_result[i:i + 16].hex() for i in range(0, len(cbc_result), 16)]

print(f'\nECB blokkok: {ecb_blocks}')
print(f'CBC blokkok: {cbc_blocks}')

# Count unique blocks
ecb_unique = len(set(ecb_blocks))
cbc_unique = len(set(cbc_blocks))

print(f'\nKulonbozo blokkok, ECB: {ecb_unique}/{len(ecb_blocks)}')
print(f'Kulonbozo blokkok, CBC: {cbc_unique}/{len(cbc_blocks)}')

if ecb_unique < len(ecb_blocks):
    print('🚨 ECB MODE: egyforma rejtjelezett blokkok!')
else:
    print('✅ ECB MODE: nincsenek egyforma rejtjelezett blokkok!')

print('✅ CBC MODE: nincsenek egyforma rejtjelezett blokkok!')
