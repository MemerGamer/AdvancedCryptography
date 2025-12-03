from Crypto.Protocol.DH import key_agreement
from Crypto.PublicKey import ECC
from Crypto.Hash import SHAKE128
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

def mkdf(x):
    return SHAKE128.new(x).read(32)

def dhRatchet(prevRootKey, privKeyAlice, pubKeyBob):
    commonSecret = key_agreement(static_priv=privKeyAlice,
                        static_pub=pubKeyBob,
                        kdf=mkdf)
    newRootKey = HKDF(commonSecret,32, prevRootKey, SHA256, 1)
    return newRootKey

rootKey = bytes.fromhex('f1df63a2ce2c70da947aab1c967e796bb84cb5f33efddf324fff73fa2a8c75b0')

oldPrivKeyBob = ECC.generate(curve='Ed25519')
oldPubKeyBob = oldPrivKeyBob.public_key()

newPrivKeyAlice = ECC.generate(curve='Ed25519')
newPubKeyAlice = newPrivKeyAlice.public_key()

newRootKey = dhRatchet(rootKey, oldPrivKeyBob, newPubKeyAlice)
print({
    "alice_new_public_key": newPubKeyAlice.export_key(format = 'raw').hex(),
    "new_root_key": newRootKey.hex()
})


