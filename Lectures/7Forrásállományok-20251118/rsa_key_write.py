from Crypto.PublicKey import RSA
import os
from dotenv import load_dotenv

def keyWrite(k, password, puKeyFile, prKeyFile):
    key = RSA.generate(k)
    with open(puKeyFile, 'wb') as f:
        f.write(key.public_key().export_key())
    with open(prKeyFile, 'wb') as f:
        f.write(key.export_key( passphrase=password, pkcs=8,
                                protection='PBKDF2WithHMAC-SHA512AndAES256-CBC'))

load_dotenv()
password = os.getenv('RSA_ENCRYPTION_PASSWORD')
if not password:
        raise ValueError("Password not found in environment variables")
puKeyFile = 'publickeyRSA.pem'
prKeyFile = 'privatekeyRSA.pem'
keyWrite(2048, password, puKeyFile, prKeyFile)
