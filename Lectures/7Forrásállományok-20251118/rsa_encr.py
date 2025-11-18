from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from dotenv import load_dotenv


def RSAOAEPencryption(mess, puKeyFile):
    temp = open(puKeyFile, 'rb').read()
    key = RSA.import_key(temp)
    cipher = PKCS1_OAEP.new(key)
    messEncr = cipher.encrypt(mess)
    return(messEncr)

def RSAOAEPdecryption(messEncr, password, prKeyFile):
    temp = open(prKeyFile, 'rb').read()
    key = RSA.import_key(temp, password)
    # print(key.q)
    # print(key.p)
    decipher = PKCS1_OAEP.new(key)
    messDecr = decipher.decrypt(messEncr)
    return messDecr

mess = os.urandom(32)
print('message: ', mess.hex())
messEncr = RSAOAEPencryption(mess, 'publickeyRSA.pem')
print('encryption: ', messEncr.hex())

load_dotenv(override=True)
password = os.getenv('RSA_ENCRYPTION_PASSWORD')
if not password:
        raise ValueError("Password not found in environment variables")
prKeyFile = 'privatekeyRSA.pem'
messDecr = RSAOAEPdecryption(messEncr, password, prKeyFile)
print('mess decryption: ', messDecr.hex())