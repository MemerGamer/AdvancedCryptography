#egy onion titkositasi muvelet soran a titositott tartalom negy retegen megy keresztul
from Crypto.Cipher import AES
import json
import os

def encrypt_AES_GCM(plaintext, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    # a tag, a nonce 16 bajtosak
    return tag + cipher.nonce + ciphertext

def onion_encrypt(data, keys):
    for key in keys:
        data = encrypt_AES_GCM(data, key)
    return data

def problem_preparation():
    key = ['nodeA_key', 'nodeB_key', 'nodeC_key', 'nodeD_key', 'ciphertext']
    plaintext = 'Tor is a free overlay network for enabling anonymous communication. It is built on free and open-source software run by over seven thousand volunteer-operated relays worldwide, as well as by millions of users who route their Internet traffic via random paths through these relays.'.encode()
    keyA = os.urandom(32)
    keyB = os.urandom(32)
    keyC = os.urandom(32)
    keyD = os.urandom(32)
    crData = onion_encrypt(plaintext, reversed([keyA, keyB, keyC, keyD]))

    value = [keyA.hex(), keyB.hex(), keyC.hex(), keyD.hex(), crData.hex()]
    onoinR = dict(zip(key, value))
    with open('onionRouting.json', 'wt') as f:
        json.dump(onoinR, f, indent=4, ensure_ascii=False)

problem_preparation()

