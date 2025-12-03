from Crypto.Hash import SHA512
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa

def keyGen(puKeyFile = 'public_ed25519.pem', prKeyFile = 'private_ed25519.pem'):
    key = ECC.generate(curve = 'ed25519')

    f = open(puKeyFile, 'wt')
    f.write(key.public_key().export_key(format='PEM'))
    f.close()

    f = open(prKeyFile, 'wt')
    f.write(key.export_key(format = 'PEM'))
    f.close()


def messSign(message = b'Tananyag Kripto msteri'):
    key = ECC.import_key(open('private_ed25519.pem').read())
    hashMessage = SHA512.new(message)
    signer = eddsa.new(key, 'rfc8032')
    signature = signer.sign(hashMessage)
    print(signature)
    f = open('signature25519.hex', 'wt')
    f.write(signature.hex())
    f.close()

def messVerify(message = b'Tananyag Kripto msteri'):
    signature = open('signature25519.hex').read()
    signature = bytes.fromhex(signature)
    key = ECC.import_key(open('public_ed25519.pem').read())
    verifier = eddsa.new(key, 'rfc8032')
    try:
        hashMessage = SHA512.new(message)
        verifier.verify(hashMessage, signature)
        print('ervenyes az alairas')
    except ValueError:
        print('ervenytelen az alairas')

def main():
    keyGen()
    messSign()
    messVerify()

main()